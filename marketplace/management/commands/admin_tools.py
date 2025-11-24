from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum, Avg
from marketplace.models import Product, Order, RatingReview, CartItem
from decimal import Decimal
import datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Comprehensive admin tools for CRUD operations and management'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            choices=[
                'stats', 'cleanup', 'approve-sellers', 'deactivate-inactive-products',
                'export-data', 'backup-data', 'restore-data', 'check-integrity'
            ],
            help='Action to perform'
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days for cleanup operations'
        )
        parser.add_argument(
            '--user-id',
            type=int,
            help='User ID for specific operations'
        )

    def handle(self, *args, **options):
        action = options.get('action')
        
        if action == 'stats':
            self.show_statistics()
        elif action == 'cleanup':
            self.cleanup_data(options.get('days'))
        elif action == 'approve-sellers':
            self.approve_pending_sellers()
        elif action == 'deactivate-inactive-products':
            self.deactivate_inactive_products(options.get('days'))
        elif action == 'export-data':
            self.export_data()
        elif action == 'backup-data':
            self.backup_data()
        elif action == 'check-integrity':
            self.check_data_integrity()
        else:
            self.show_help()

    def show_statistics(self):
        """Show comprehensive statistics"""
        self.stdout.write(self.style.SUCCESS('=== KAUMAHAN HARVEST MARKET STATISTICS ==='))
        
        # User Statistics
        total_users = User.objects.count()
        sellers = User.objects.filter(user_type='seller').count()
        buyers = User.objects.filter(user_type='buyer').count()
        approved_sellers = User.objects.filter(user_type='seller', is_approved=True).count()
        pending_sellers = User.objects.filter(user_type='seller', is_approved=False).count()
        
        self.stdout.write(f'\n👥 USERS:')
        self.stdout.write(f'  Total Users: {total_users}')
        self.stdout.write(f'  Sellers: {sellers} (Approved: {approved_sellers}, Pending: {pending_sellers})')
        self.stdout.write(f'  Buyers: {buyers}')
        
        # Product Statistics
        total_products = Product.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        inactive_products = Product.objects.filter(is_active=False).count()
        
        self.stdout.write(f'\n📦 PRODUCTS:')
        self.stdout.write(f'  Total Products: {total_products}')
        self.stdout.write(f'  Active Products: {active_products}')
        self.stdout.write(f'  Inactive Products: {inactive_products}')
        
        # Order Statistics
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status='PENDING').count()
        confirmed_orders = Order.objects.filter(status='CONFIRMED').count()
        shipped_orders = Order.objects.filter(status='SHIPPED').count()
        delivered_orders = Order.objects.filter(status='DELIVERED').count()
        cancelled_orders = Order.objects.filter(status='CANCELLED').count()
        
        total_revenue = Order.objects.filter(status='DELIVERED').aggregate(
            total=Sum('total_amount')
        )['total'] or Decimal('0')
        
        self.stdout.write(f'\n🛒 ORDERS:')
        self.stdout.write(f'  Total Orders: {total_orders}')
        self.stdout.write(f'  Pending: {pending_orders}')
        self.stdout.write(f'  Confirmed: {confirmed_orders}')
        self.stdout.write(f'  Shipped: {shipped_orders}')
        self.stdout.write(f'  Delivered: {delivered_orders}')
        self.stdout.write(f'  Cancelled: {cancelled_orders}')
        self.stdout.write(f'  Total Revenue: ₱{total_revenue:,.2f}')
        
        # Review Statistics
        total_reviews = RatingReview.objects.count()
        approved_reviews = RatingReview.objects.filter(is_approved=True).count()
        pending_reviews = RatingReview.objects.filter(is_approved=False).count()
        avg_rating = RatingReview.objects.filter(is_approved=True).aggregate(
            avg=Avg('rating')
        )['avg'] or 0
        
        self.stdout.write(f'\n⭐ REVIEWS:')
        self.stdout.write(f'  Total Reviews: {total_reviews}')
        self.stdout.write(f'  Approved: {approved_reviews}')
        self.stdout.write(f'  Pending: {pending_reviews}')
        self.stdout.write(f'  Average Rating: {avg_rating:.1f}/5')
        
        # Cart Statistics
        active_carts = CartItem.objects.values('user').distinct().count()
        total_cart_items = CartItem.objects.count()
        
        self.stdout.write(f'\n🛒 CART:')
        self.stdout.write(f'  Active Carts: {active_carts}')
        self.stdout.write(f'  Total Cart Items: {total_cart_items}')

    def cleanup_data(self, days):
        """Clean up old data"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        
        # Clean up old cart items
        old_cart_items = CartItem.objects.filter(added_at__lt=cutoff_date)
        cart_count = old_cart_items.count()
        old_cart_items.delete()
        
        self.stdout.write(self.style.SUCCESS(f'Cleaned up {cart_count} old cart items'))
        
        # Clean up cancelled orders older than specified days
        old_cancelled_orders = Order.objects.filter(
            status='CANCELLED', 
            created_at__lt=cutoff_date
        )
        order_count = old_cancelled_orders.count()
        old_cancelled_orders.delete()
        
        self.stdout.write(self.style.SUCCESS(f'Cleaned up {order_count} old cancelled orders'))

    def approve_pending_sellers(self):
        """Approve all pending sellers"""
        pending_sellers = User.objects.filter(user_type='seller', is_approved=False)
        count = pending_sellers.count()
        
        if count == 0:
            self.stdout.write(self.style.WARNING('No pending sellers to approve'))
            return
        
        pending_sellers.update(is_approved=True)
        self.stdout.write(self.style.SUCCESS(f'Approved {count} sellers'))

    def deactivate_inactive_products(self, days):
        """Deactivate products without orders in specified days"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        
        # Find products that haven't been ordered in the specified period
        inactive_products = Product.objects.filter(
            is_active=True
        ).exclude(
            orderitem__order__created_at__gte=cutoff_date
        )
        
        count = inactive_products.count()
        if count == 0:
            self.stdout.write(self.style.WARNING('No inactive products to deactivate'))
            return
        
        inactive_products.update(is_active=False)
        self.stdout.write(self.style.SUCCESS(f'Deactivated {count} inactive products'))

    def export_data(self):
        """Export important data for backup"""
        import csv
        import os
        
        # Create exports directory if it doesn't exist
        os.makedirs('exports', exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Export users
        with open(f'exports/users_{timestamp}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Email', 'Full Name', 'User Type', 'Is Approved', 'Date Joined'])
            
            for user in User.objects.all():
                writer.writerow([
                    user.id, user.email, user.full_name, 
                    user.user_type, user.is_approved, user.date_joined
                ])
        
        # Export products
        with open(f'exports/products_{timestamp}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Seller', 'Price', 'Category', 'Is Active', 'Created At'])
            
            for product in Product.objects.all():
                writer.writerow([
                    product.id, product.name, product.seller.email,
                    product.price, product.category, product.is_active, product.created_at
                ])
        
        # Export orders
        with open(f'exports/orders_{timestamp}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Buyer', 'Seller', 'Total Amount', 'Status', 'Created At'])
            
            for order in Order.objects.all():
                writer.writerow([
                    order.id, order.buyer.email, order.seller.email,
                    order.total_amount, order.status, order.created_at
                ])
        
        self.stdout.write(self.style.SUCCESS(f'Data exported to exports/ directory with timestamp {timestamp}'))

    def backup_data(self):
        """Create a simple data backup"""
        self.stdout.write(self.style.WARNING('Note: For production, use proper database backup tools'))
        self.export_data()

    def check_data_integrity(self):
        """Check data integrity and report issues"""
        self.stdout.write(self.style.SUCCESS('=== DATA INTEGRITY CHECK ==='))
        
        issues_found = 0
        
        # Check for products with invalid sellers
        invalid_products = Product.objects.filter(seller__isnull=True)
        if invalid_products.exists():
            issues_found += 1
            self.stdout.write(self.style.ERROR(f'Found {invalid_products.count()} products with invalid sellers'))
        
        # Check for orders with invalid users
        invalid_orders = Order.objects.filter(buyer__isnull=True) | Order.objects.filter(seller__isnull=True)
        if invalid_orders.exists():
            issues_found += 1
            self.stdout.write(self.style.ERROR(f'Found {invalid_orders.count()} orders with invalid users'))
        
        # Check for cart items with invalid products or users
        invalid_cart_items = CartItem.objects.filter(product__isnull=True) | CartItem.objects.filter(user__isnull=True)
        if invalid_cart_items.exists():
            issues_found += 1
            self.stdout.write(self.style.ERROR(f'Found {invalid_cart_items.count()} cart items with invalid references'))
        
        # Check for reviews with invalid products or users
        invalid_reviews = RatingReview.objects.filter(product__isnull=True) | RatingReview.objects.filter(buyer__isnull=True)
        if invalid_reviews.exists():
            issues_found += 1
            self.stdout.write(self.style.ERROR(f'Found {invalid_reviews.count()} reviews with invalid references'))
        
        if issues_found == 0:
            self.stdout.write(self.style.SUCCESS('✅ No data integrity issues found'))
        else:
            self.stdout.write(self.style.ERROR(f'❌ Found {issues_found} data integrity issues'))

    def show_help(self):
        """Show help information"""
        self.stdout.write(self.style.SUCCESS('=== ADMIN TOOLS HELP ==='))
        self.stdout.write('Available actions:')
        self.stdout.write('  stats                    - Show comprehensive statistics')
        self.stdout.write('  cleanup                  - Clean up old data')
        self.stdout.write('  approve-sellers          - Approve all pending sellers')
        self.stdout.write('  deactivate-inactive-products - Deactivate inactive products')
        self.stdout.write('  export-data              - Export data to CSV files')
        self.stdout.write('  backup-data              - Create data backup')
        self.stdout.write('  check-integrity          - Check data integrity')
        self.stdout.write('')
        self.stdout.write('Examples:')
        self.stdout.write('  python manage.py admin_tools --action=stats')
        self.stdout.write('  python manage.py admin_tools --action=cleanup --days=60')
        self.stdout.write('  python manage.py admin_tools --action=approve-sellers')
