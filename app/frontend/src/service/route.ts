import loadRacinginfo from "./api/racinginfo";

type RouterType = {
    init: () => void;
    go: (route: string, addToHistory?: boolean) => void;
};

const Router: RouterType = {
    init: () => {
        document.querySelectorAll("a.navlink").forEach((a) => {
            a.addEventListener("click", (event) => {
                event.preventDefault();
                const target = event.target as HTMLAnchorElement;
                const url = target.getAttribute("href");
                if (!url) {
                    return;
                }
                Router.go(url);
            });
        });
        window.addEventListener("popstate", (event) => {
            Router.go(event.state.route, false);
        });

        Router.go(location.pathname);
    },
    go: (route, addToHistory = true) => {
        if (addToHistory) {
            history.pushState({ route }, "", route);
        }
        let pageElement = null;
        switch (route) {
            case "/": {
                pageElement = document.createElement("app-home-page");
                break;
            }
            case "/race": {
                console.log("inrace", window.app.store.hasOwnProperty("racingInfo"));
                if (window.app.store.hasOwnProperty("racingInfo")) {
                    console.log("already loaded");
                    loadRacinginfo();
                }
                pageElement = document.createElement("app-race-page");
                break;
            }
            default: {
                pageElement = document.createElement("app-home-page");
                break;
            }
        }
        if (pageElement) {
            const cache = document.querySelector("main");
            if (!cache) {
                return;
            }
            cache.innerHTML = "";
            cache.appendChild(pageElement);
            window.scrollX = 0;
            window.scrollY = 0;
        } else {
            const cache = document.querySelector("main");
            if (!cache) {
                return;
            }
            cache.innerHTML = "Oups, 404!";
        }
    },
};
export default Router;
