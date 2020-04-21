import _ from "lodash";

export function reformatTable(tableData) {
  const res = {
    table_data: tableData,
    table_titles: _.chain(Object.keys(tableData[0]))
      .map(function(item) {
        return {
          key: item,
          label: item,
          sortable: true
        };
      })
      .value()
  };
  return res;
}
