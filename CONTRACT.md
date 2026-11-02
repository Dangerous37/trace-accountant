# Span contract
spans are unique IDs with parent (null at roots), start and end integer ticks (end may be null). Complete child spans must fit inside complete parents. For each complete span, subtract the union of its direct children's intervals. Exclude spans with incomplete direct children from bottleneck ranking. Report the largest attributable exclusive span and all incomplete IDs.
