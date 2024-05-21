import message from "./message";

function matchArray<T extends any>(value: T[], comparer: T[]) {
    if (value.length === comparer.length) {
        for (let i = 0; i < value.length; i++) {
            if (value[i] !== comparer[i]) {
                return false;
            }
        }
        return true;
    } else {
        return false;
    }
}

export default function match<C extends any, T extends any>(
    value: C,
    comparer: T,
) {
    if (Array.isArray(value) && Array.isArray(comparer)) {
        const ok = matchArray(value, comparer);
        return {
            ok,
            message: message(ok, value, comparer),
        };
    }
    // @ts-ignore
    if (value === comparer) {
        const ok = true;
        return {
            ok,
            message: message(ok, value, comparer),
        };
    } else {
        const ok = false;
        return {
            ok,
            message: message(ok, value, comparer),
        };
    }
}
