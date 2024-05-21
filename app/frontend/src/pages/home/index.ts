import Component from "../../service/component";

class Home extends Component {
    constructor() {
        super();
    }

    getModuleUrl() {
        return import.meta.url;
    }
}

export default customElements.define("app-home-page", Home);
