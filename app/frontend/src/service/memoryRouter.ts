import { RouteEvents } from "./events/route";
import customLocalStorage from "./storage/localStorage";

type IMemoryRouter = {
  currentRoute: string;
  memory: string[];
  debug: boolean;
};
const MEMORY_ROUTER_STORE = "memoryRouterStore";

const memoryLocalStorage =
  customLocalStorage<IMemoryRouter>(MEMORY_ROUTER_STORE);

const MemoryRouter: IMemoryRouter = {
  currentRoute: "home",
  memory: ["home"],
  debug: false,
};
function setCurrentRoute(
  store: IMemoryRouter,
  prop: keyof IMemoryRouter,
  value: string,
) {
  if (prop === "currentRoute") {
    store[prop] = value;
    window.dispatchEvent(new Event(RouteEvents.changeroute));
  }
}

const memoryRouterStore = new Proxy<IMemoryRouter>(MemoryRouter, {
  set: (store: IMemoryRouter, prop: keyof IMemoryRouter, value: string) => {
    setCurrentRoute(store, prop, value);
    if (prop === "debug") {
      // @ts-ignore
      store[prop] = value;
    }
    if (prop === "memory") {
      // @ts-ignore
      store[prop] = value;
    }
    return true;
  },
});

function addPageToCurrentRoute(document: Document, wrapper: HTMLElement) {
  return (path: string) => {
    function addContainerChild(parent: HTMLElement, child: HTMLElement) {
      parent.innerHTML = "";
      wrapper.appendChild(child);
    }
    const correctPagePath = `app-${path}-page`;
    const pageElement = document.createElement(correctPagePath);
    addContainerChild(wrapper, pageElement);
  };
}
interface RouteBackEventDetail {
  // Add any properties that your custom event might have
  path: string;
}
// Step 3: Extend the WindowEventMap
interface CustomWindowEventMap extends WindowEventMap {
  "route:back": CustomEvent<RouteBackEventDetail>;
}

const eventMap = {
  popstate: "popstate",
  hashchange: "hashchange",
  beforeunload: "beforeunload",
  unload: "unload",
} as const;

function embeddedRouterEvents(document: Document, wrapper: HTMLElement) {
  const parent = addPageToCurrentRoute(document, wrapper);
  Object.keys(eventMap).forEach((key) => {
    window.addEventListener(key, (event) => {
      // @ts-ignore
      const route: string | null = event?.state.route;

      if (route === null) {
        // first page
        return;
      }

      const idx = memoryRouterStore.memory.indexOf(route);

      if (idx === memoryRouterStore.memory.length - 1) {
        onRouteModify(window, route, "forward");
        return parent(route);
      }

      onRouteModify(window, route, "back");
      return parent(route);
    });
  });
}

export const addRouterPositionInMemory = (
  memory: string[],
  route: string,
  direction: "forward" | "back",
) => {
  if (direction === "forward") {
    const currentMemory = memory.filter((x) => x !== route);
    currentMemory.push(route);
    return currentMemory;
  }

  memory.pop();
  return memory;
};
type ParentType = ReturnType<typeof addPageToCurrentRoute>;

function onRouteBack(parent: ParentType) {
  return (_: Event) => {
    // #TODO should handle the case when the memory is empty
    if (memoryRouterStore.memory.length <= 1) {
      return;
    }

    window.app.memoryRouter.store.memory.pop();
    const stack = window.app.memoryRouter.store.memory;
    const nextRoute = stack[stack.length - 1];
    if (!nextRoute) {
      return;
    }

    window.app.memoryRouter.store.currentRoute = nextRoute;
    parent(nextRoute);

    history.pushState({ route: nextRoute }, "", "");

    const debug = window.app.memoryRouter.store.debug;
    if (debug) {
      memoryLocalStorage.set(
        MEMORY_ROUTER_STORE,
        window.app.memoryRouter.store,
      );
    }
  };
}

function onRouteChange(parent: ParentType) {
  return (_: Event) => {
    const path = memoryRouterStore.currentRoute;
    history.pushState({ route: path }, "", "");
    onRouteModify(window, memoryRouterStore.currentRoute, "forward");
    parent(path);
  };
}

function onRouteModify(
  window: Window,
  route: string,
  type: "forward" | "back",
) {
  window.app.memoryRouter.store.memory = addRouterPositionInMemory(
    memoryRouterStore.memory,
    route,
    type,
  );

  const debug = window.app.memoryRouter.store.debug;
  if (debug) {
    memoryLocalStorage.set(MEMORY_ROUTER_STORE, window.app.memoryRouter.store);
  }
}

function MemoryRouterContext(
  window: Window,
  document: Document,
  wrapper: HTMLElement,
  debug = false,
) {
  const parent = addPageToCurrentRoute(document, wrapper);
  const onRouteBackEventHandler = onRouteBack(parent);
  const onRouteChangeEventHandler = onRouteChange(parent);

  history.replaceState({ route: null, pivot: null }, "", "");

  window.app.memoryRouter.store.debug = debug;
  if (debug) {
    const storageMemory = memoryLocalStorage.get(MEMORY_ROUTER_STORE)?.memory;
    const storageCurrentRoute =
      memoryLocalStorage.get(MEMORY_ROUTER_STORE)?.currentRoute;

    if (storageMemory) {
      window.app.memoryRouter.store.memory = storageMemory;
    }
    if (storageCurrentRoute) {
      window.app.memoryRouter.store.currentRoute = storageCurrentRoute;
      parent(storageCurrentRoute);
    }
  }

  window.addEventListener(
    RouteEvents.changeroute,
    onRouteChangeEventHandler,
    false,
  );
  window.addEventListener(RouteEvents.back, onRouteBackEventHandler, false);
}

export default {
  store: memoryRouterStore,
  context: MemoryRouterContext,
  embeddedRouterEvents: embeddedRouterEvents,
};
