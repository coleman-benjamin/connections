#### Degrees of Separation

### Challenges
- Would want to include already fetched Person Ids to exclude in each subsequent query for connections (as in `WHERE to_person_id NOT IN ([ids])`)
- Must provide failover strategy for cases when the number of specified degrees can't be fulfilled, e.g. at whatever point the query returns 0 results
- Would be wise to consider what the maximum number of degrees of separation are mathmatically feesible given the size or potential of the dataset
- Given a large dataset and high degree numbers, would require performance testing, might need to apply a limit of degrees

### Questions for PO
- Use cases?
- Are you concerned with displaying results in terms of or having any notion of how many degrees each Person is seperated by?