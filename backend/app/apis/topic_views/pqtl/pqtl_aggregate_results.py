def pqtl_aggregate_results(results, search_flag):
    """Aggregates some of the results' parameters into the lists
    to display in Basic summary.
    """

    # Initialize all lists
    (
        aggr_list,
        list_rs_ID,
        list_cis,
        list_direct,
        list_pleio,
        list_coloc,
        new_rows,
    ) = ([] for _ in range(7))

    if search_flag == "proteins":
        aggr_index = 2
    else:
        aggr_index = 0

    # Init variables
    exp = None
    trait = None
    out = None
    mr_pvalue = None
    hetero_test = None

    for i, rows in enumerate(results):

        if rows[aggr_index] not in aggr_list and len(aggr_list) > 0:
            if search_flag == "proteins":
                new_rows.append(
                    [
                        exp,
                        trait,
                        aggr_list[0],
                        mr_pvalue,
                        hetero_test,
                        ",\n".join(list_rs_ID),
                        ",\n".join(list_cis),
                        ",\n".join(list_direct),
                        ",".join(str(x) for x in list_pleio),
                        ",\n".join(list_coloc),
                    ]
                )

                # Set to empty all lists
                (
                    aggr_list,
                    list_rs_ID,
                    list_cis,
                    list_direct,
                    list_pleio,
                    list_coloc,
                ) = ([] for _ in range(6))

                # Record new data
                exp = rows[0]

            else:
                new_rows.append(
                    [
                        aggr_list[0],
                        trait,
                        out,
                        mr_pvalue,
                        hetero_test,
                        ",\n".join(list_rs_ID),
                        ",\n".join(list_cis),
                        ",\n".join(list_direct),
                        ",".join(str(x) for x in list_pleio),
                        ",\n".join(list_coloc),
                    ]
                )

                # Set to empty all lists
                (
                    aggr_list,
                    list_rs_ID,
                    list_cis,
                    list_direct,
                    list_pleio,
                    list_coloc,
                ) = ([] for j in range(6))

                # Record new data
                out = rows[2]

            aggr_list.append(rows[aggr_index])
            trait = rows[1]
            list_rs_ID.append(rows[5])
            mr_pvalue = rows[3]
            list_cis.append(rows[6])
            list_direct.append(rows[7])
            list_pleio.append(rows[8])
            list_coloc.append(rows[9])
            hetero_test = rows[4]

        else:
            if rows[aggr_index] not in aggr_list:
                if search_flag == "proteins":
                    exp = rows[0]
                else:
                    out = rows[2]

                aggr_list.append(rows[aggr_index])
                trait = rows[1]
                list_rs_ID.append(rows[5])
                mr_pvalue = rows[3]
                list_cis.append(rows[6])
                list_direct.append(rows[7])
                list_pleio.append(rows[8])
                list_coloc.append(rows[9])
                hetero_test = rows[4]

            else:
                list_rs_ID.append(rows[5])
                list_cis.append(rows[6])
                list_direct.append(rows[7])
                list_pleio.append(rows[8])
                list_coloc.append(rows[9])

        if i == len(results) - 1:
            if search_flag == "proteins":
                new_rows.append(
                    [
                        exp,
                        trait,
                        aggr_list[0],
                        mr_pvalue,
                        hetero_test,
                        ",\n".join(list_rs_ID),
                        ",\n".join(list_cis),
                        ",\n".join(list_direct),
                        ",".join(str(x) for x in list_pleio),
                        ",\n".join(list_coloc),
                    ]
                )
            else:
                new_rows.append(
                    [
                        aggr_list[0],
                        trait,
                        out,
                        mr_pvalue,
                        hetero_test,
                        ",\n".join(list_rs_ID),
                        ",\n".join(list_cis),
                        ",\n".join(list_direct),
                        ",".join(str(x) for x in list_pleio),
                        ",\n".join(list_coloc),
                    ]
                )
    return new_rows
