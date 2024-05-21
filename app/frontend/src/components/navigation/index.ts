import Component from "../../service/component";

// required prod in the webcomponent
// path the current path to the new frame
class Navigation extends Component {
  static observedAttributes = ["path"];

  path: string = "";

  constructor() {
    super({
      loaded: (node) => this.attachEventHandlers(node),
    });
  }

  getModuleUrl() {
    return import.meta.url;
  }

  attributeChangedCallback(name: string, oldValue: string, newValue: string) {
    if (name === "path" && oldValue !== newValue) {
      this.path = newValue;
    }
  }
  attachEventHandlers(node: ShadowRoot) {
    const button = node.querySelector("#app-navigation");

    if (button) {
      button.addEventListener("click", () => {
        this.handleButtonClick();
      });
    }
  }

  handleButtonClick() {
    if (this.path !== "") {
      window.app.memoryRouter.store.currentRoute = this.path;
    }
  }
}

export default customElements.define("app-navigation", Navigation);
