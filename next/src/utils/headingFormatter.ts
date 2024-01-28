export function formatHeader(str: string) {
  const words = str.split("_");

  return words
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}
