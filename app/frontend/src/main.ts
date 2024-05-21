import "./input.css";
import "./components";
import "./pages";
import "./header";
import Router from "./service/route";
import store from "./service/store";
import { RacingInfo } from "../wailsjs/go/main/App";
import memoryRouter from "./service/memoryRouter";

type MyApp = {
  router: typeof Router;
  store: typeof store;
  memoryRouter: typeof memoryRouter;
};
window.horse = function () {
  try {
    RacingInfo("")
      .then((result) => {
        if (window.app.store === undefined) {
          return;
        }
        // console.log("racingInfo result ---------->", result);
        if (result) {
          const racingInfoValues = JSON.parse(result);
          console.log("racingInfoValues ---------->", racingInfoValues);
          window.app.store.racingInfo = JSON.parse(result);
        }
      })
      .catch((err) => {
        throw new Error(err);
      });
  } catch (err) {
    console.log("racingInfo not loaded", err);
  }
  console.log("racingInfo loaded");
};

let app = {} as MyApp;
app.router = Router;
app.store = store;
app.memoryRouter = memoryRouter;

window.app = app;

window.addEventListener("DOMContentLoaded", () => {
  Router.init();
  const wrapper = document.querySelector("main") as HTMLElement;

  memoryRouter.context(window, document, wrapper, true);

  memoryRouter.embeddedRouterEvents(document, wrapper);
});

declare global {
  interface Window {
    greet: () => void;
    horse: () => void;
    app: MyApp;
  }
}
