export default function message<T extends any, C extends any>(
    ok: boolean,
    value: T,
    comparer: C,
) {
    if (ok) {
        return `${value} "==="  ${comparer}`;
    }
    return `${value} "!=="  ${comparer}`;
}
