import _ from "lodash";

export function hexToRGB(hex, alpha) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  if (alpha) {
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  } else {
    return `rgb(${r}, ${g}, ${b})`;
  }
}

export function formatLabel(label) {
  const charLimit = 20;
  const truncated = label.substring(0, charLimit);
  const wrapLabel = _.chain(truncated.split(/(\s+)/))
    .filter(e => /\S/.test(e))
    .map(e => {
      const limit = 10;
      let res;
      if (e.length > limit) {
        res = e.substring(0, limit) + "...";
      } else {
        res = e;
      }
      return res;
    })
    .reduce((a, b) => a + "\n" + b)
    .value();
  const res = wrapLabel;
  return res;
}
