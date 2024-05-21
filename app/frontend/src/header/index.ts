import Component from "../service/component";
import { RouteEvents } from "../service/events/route";

class Header extends Component {
  constructor() {
    console.log("Header");
    super({ loaded: (node) => this.attachEventHandlers(node) });
  }

  getModuleUrl() {
    return import.meta.url;
  }

  attachEventHandlers(node: ShadowRoot) {
    const button = node.querySelector("#app-header-back-button");
    if (button) {
      button.addEventListener("click", () => {
        window.dispatchEvent(new CustomEvent(RouteEvents.back));
      });
    }
  }
}
export default customElements.define("app-header", Header);
