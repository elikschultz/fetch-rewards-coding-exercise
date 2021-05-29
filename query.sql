select
	rewardsReceiptStatus,
	avg(totalSpent) as average_spend,
	sum(purchasedItemCount) as total_items
from fact_receipt
where rewardsReceiptStatus in ('ACCEPTED', 'REJECTED')
group by 1
