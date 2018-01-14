select c_mktsegment, count(*)
from customer
group by c_mktsegment
order by c_mktsegment
