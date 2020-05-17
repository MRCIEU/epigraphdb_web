export let web_backend_url = "";

if (process.env.VUE_APP_WEB_BACKEND_URL) {
  web_backend_url = `${process.env.VUE_APP_WEB_BACKEND_URL}`;
} else {
  web_backend_url = null;
  console.error("web_backend_url not set!");
}

export let web_debug = false;

if (process.env.VUE_APP_DEBUG) {
  web_debug = process.env.VUE_APP_DEBUG;
}

if (web_debug) {
  console.log(process.env.VUE_APP_API_URL);
}

export let gtagId = process.env.VUE_APP_GTAG_ID
  ? process.env.VUE_APP_GTAG_ID
  : null;
