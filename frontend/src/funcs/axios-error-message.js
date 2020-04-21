export const axiosErrorMessage = function(error) {
  if (error.response) {
    console.log(error.request);
    console.log(error.response.data);
    console.log(error.response.status);
    console.log(error.response.headers);
  } else if (error.request) {
    console.error(error.request);
  } else {
    console.error(error.message);
  }
};
