import Component from "../../service/component";

class Card extends Component {
  constructor() {
    super();
  }
  getModuleUrl() {
    return import.meta.url;
  }
}
export default customElements.define("app-card", Card);
