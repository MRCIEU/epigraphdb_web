import axios from "axios";

export function axiosDownload(url, params) {
  axios.get(url, { params: params, responseType: "blob" }).then(response => {
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const contentDisposition = response.headers["content-disposition"];
    let fileName = "unknown";
    if (contentDisposition) {
      const fileNameMatch = contentDisposition.match(/filename=(.+)/);
      if (fileNameMatch.length === 2) {
        fileName = fileNameMatch[1];
      }
    }
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", fileName);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  });
}
