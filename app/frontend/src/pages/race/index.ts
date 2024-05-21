import Component from "../../service/component";

class Race extends Component {
    constructor() {
        super();
        window.horse();
    }
    getModuleUrl() {
        return import.meta.url;
    }
}

export default customElements.define("app-race-page", Race);
