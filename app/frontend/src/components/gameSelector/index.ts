import Component from "../../service/component";
function loader(node: ShadowRoot) {
  const racingInfo = window.app.store.racingInfo;
  if (!racingInfo) {
    return;
  }
  // @ts-ignore
  const entries = Object.entries(racingInfo.games);
  const container = node.getElementById("app-game-selector-list");

  entries?.forEach(([key, _]: [key: string, value: any]) => {
    const gameCard = document.createElement("app-card");
    const h2 = document.createElement("h2");
    h2.innerText = key;
    gameCard.appendChild(h2);
    container?.appendChild(gameCard);
  });

  if (!container) {
    return;
  }

  node.appendChild(container);
}
class GameSelector extends Component {
  constructor() {
    super({ loaded: loader });
  }

  getModuleUrl() {
    return import.meta.url;
  }
}
export default customElements.define("app-game-selector", GameSelector);
