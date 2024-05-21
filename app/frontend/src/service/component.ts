interface IComponent extends HTMLElement {
    fetchHtmlMarkup(): Promise<string>;
    injectGlobalStyles(): void;
    render(): Promise<void>;
    getModuleUrl(): string;
}

type Contructor = {
    loaded?: (root: ShadowRoot) => void;
};
abstract class Component extends HTMLElement implements IComponent {
    root: ShadowRoot;

    htmlCache: string | null = null;
    loaded?: (root: ShadowRoot) => void | undefined;

    constructor(props?: Contructor) {
        super();
        this.root = this.attachShadow({ mode: "open" });
        this.fetchAndRenderHtml();
        if (props?.loaded) {
            this.loaded = props.loaded;
        }
    }

    abstract getModuleUrl(): string;

    async fetchHtmlMarkup(): Promise<string> {
        if (this.htmlCache) {
            return this.htmlCache;
        } else {
            try {
                const importPath = new URL(this.getModuleUrl());
                const htmlPath = importPath.pathname.replace("index.ts", "markup.html");
                const response = await fetch(htmlPath);

                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }

                const html = await response.text();
                this.htmlCache = html; // Cache the fetched HTML content
                return html;
            } catch (error) {
                throw new Error("Error loading the home html file");
            }
        }
    }

    injectGlobalStyles() {
        const globalStyleSheet = Array.from(document.styleSheets);

        for (const styleSheet of globalStyleSheet) {
            if (styleSheet && styleSheet.cssRules) {
                const styleElement = document.createElement("style");
                try {
                    Array.from(styleSheet.cssRules).forEach((rule) => {
                        styleElement.appendChild(document.createTextNode(rule.cssText));
                    });
                    this.root.appendChild(styleElement);
                } catch (e) {
                    console.error("Could not copy CSS rules: ", e);
                }
            }
        }
    }

    async fetchAndRenderHtml(): Promise<void> {
        try {
            const html = await this.fetchHtmlMarkup();
            this.root.innerHTML = html;
            this.injectGlobalStyles();

            this.loaded?.(this.root);
        } catch (error) {
            console.error("Error loading the home html file", error);
        }
    }

    async render(): Promise<void> {
        console.log("do some rendering");
    }
}
export default Component;
