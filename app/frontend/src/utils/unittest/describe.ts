// Describe test function
export default function describe(
    message: string,
    callback: (...args: any) => any,
) {
    console.log(`DESCRIBE: ${message}`);
    callback();
}
