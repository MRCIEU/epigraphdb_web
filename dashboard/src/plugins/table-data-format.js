import _ from "lodash";

export function tableFormatter(jsonData) {
  // const tableData = _.chain(jsonData.results)
  //   .map(function(item) {
  //     return item["n"];
  //   })
  //   .value();
  const tableData = jsonData;
  const tableFields = _.chain(Object.keys(tableData[0]))
    .map(function(item) {
      return {
        key: item,
        label: item,
        sortable: true
      };
    })
    .value();
  return {
    table_data: tableData,
    table_titles: tableFields
  };
}
