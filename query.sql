select
	rewardsReceiptStatus,
	avg(totalSpent) as average_spend,
	sum(purchasedItemCount) as total_items
from fact_receipt
group by 1
