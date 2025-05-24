import datetime
import json
from collections import defaultdict

class OnlineLibrarySystem:
    def __init__(self):
        # Initialize data structures for SQA activities
        self.books = {}
        self.users = {}
        self.change_log = []
        self.defects = []
        self.audit_log = []
        self.performance_metrics = {
            'book_checkouts': 0,
            'user_logins': 0,
            'search_queries': 0,
            'response_times': []
        }
        
        # Load initial data
        self._initialize_data()
        
    def _initialize_data(self):
        """Initialize with some sample data"""
        self.books = {
            '001': {'title': 'Python Programming', 'author': 'John Smith', 'status': 'available'},
            '002': {'title': 'Database Systems', 'author': 'Alice Johnson', 'status': 'available'},
            '003': {'title': 'Web Development', 'author': 'Mike Brown', 'status': 'checked_out'}
        }
        
        self.users = {
            '1001': {'name': 'Student A', 'email': 'a@university.edu', 'books_checked_out': []},
            '1002': {'name': 'Student B', 'email': 'b@university.edu', 'books_checked_out': ['003']}
        }

    # Core Library Functions
    def checkout_book(self, user_id, book_id):
        """Check out a book from the library"""
        if book_id not in self.books:
            self._log_defect(f"Book ID {book_id} not found during checkout attempt")
            return False
            
        if user_id not in self.users:
            self._log_defect(f"User ID {user_id} not found during checkout attempt")
            return False
            
        if self.books[book_id]['status'] != 'available':
            return False
            
        # Record change
        change_details = {
            'operation': 'checkout',
            'user_id': user_id,
            'book_id': book_id,
            'timestamp': str(datetime.datetime.now())
        }
        self._log_change(change_details)
        
        # Update records
        self.books[book_id]['status'] = 'checked_out'
        self.users[user_id]['books_checked_out'].append(book_id)
        self.performance_metrics['book_checkouts'] += 1
        
        # Audit the transaction
        self._log_audit('checkout', user_id, book_id)
        
        return True

    def return_book(self, user_id, book_id):
        """Return a book to the library"""
        if book_id not in self.books:
            self._log_defect(f"Book ID {book_id} not found during return attempt")
            return False
            
        if user_id not in self.users:
            self._log_defect(f"User ID {user_id} not found during return attempt")
            return False
            
        if self.books[book_id]['status'] != 'checked_out':
            return False
            
        if book_id not in self.users[user_id]['books_checked_out']:
            self._log_defect(f"Book {book_id} not checked out by user {user_id} but return attempted")
            return False
            
        # Record change
        change_details = {
            'operation': 'return',
            'user_id': user_id,
            'book_id': book_id,
            'timestamp': str(datetime.datetime.now())
        }
        self._log_change(change_details)
        
        # Update records
        self.books[book_id]['status'] = 'available'
        self.users[user_id]['books_checked_out'].remove(book_id)
        
        # Audit the transaction
        self._log_audit('return', user_id, book_id)
        
        return True

    def search_books(self, query):
        """Search for books by title or author"""
        start_time = datetime.datetime.now()
        results = []
        
        for book_id, book in self.books.items():
            if query.lower() in book['title'].lower() or query.lower() in book['author'].lower():
                results.append(book)
                
        end_time = datetime.datetime.now()
        response_time = (end_time - start_time).total_seconds()
        
        # Record performance metric
        self.performance_metrics['search_queries'] += 1
        self.performance_metrics['response_times'].append(response_time)
        
        return results

    # SQA Functions
    def _log_change(self, change_details):
        """Log changes to the system for change control"""
        self.change_log.append(change_details)
        
    def _log_defect(self, description):
        """Log defects encountered in the system"""
        defect = {
            'id': len(self.defects) + 1,
            'description': description,
            'status': 'open',
            'timestamp': str(datetime.datetime.now()),
            'severity': 'medium'
        }
        self.defects.append(defect)
        
    def _log_audit(self, action, user_id, book_id=None):
        """Log audit trail for security and compliance"""
        audit_record = {
            'action': action,
            'user_id': user_id,
            'book_id': book_id,
            'timestamp': str(datetime.datetime.now()),
            'system_state': self._get_system_snapshot()
        }
        self.audit_log.append(audit_record)
        
    def _get_system_snapshot(self):
        """Get a snapshot of critical system data for auditing"""
        return {
            'total_books': len(self.books),
            'total_users': len(self.users),
            'books_checked_out': sum(1 for book in self.books.values() if book['status'] == 'checked_out')
        }
        
    # SQA Reporting Functions
    def get_change_report(self):
        """Generate a change control report"""
        report = {
            'total_changes': len(self.change_log),
            'recent_changes': self.change_log[-5:] if len(self.change_log) > 5 else self.change_log,
            'changes_by_type': defaultdict(int)
        }
        
        for change in self.change_log:
            report['changes_by_type'][change['operation']] += 1
            
        return report
        
    def get_defect_report(self):
        """Generate a defect tracking report"""
        open_defects = [d for d in self.defects if d['status'] == 'open']
        closed_defects = [d for d in self.defects if d['status'] == 'closed']
        
        return {
            'total_defects': len(self.defects),
            'open_defects': len(open_defects),
            'closed_defects': len(closed_defects),
            'defects_by_severity': defaultdict(int)
        }
        
    def get_audit_report(self):
        """Generate an audit report"""
        return {
            'total_audit_entries': len(self.audit_log),
            'recent_activities': self.audit_log[-5:] if len(self.audit_log) > 5 else self.audit_log,
            'activities_by_type': defaultdict(int)
        }
        
    def get_performance_report(self):
        """Generate a performance report"""
        response_times = self.performance_metrics['response_times']
        avg_response_time = sum(response_times)/len(response_times) if response_times else 0
        
        return {
            'book_checkouts': self.performance_metrics['book_checkouts'],
            'user_logins': self.performance_metrics['user_logins'],
            'search_queries': self.performance_metrics['search_queries'],
            'average_response_time': avg_response_time,
            'performance_trend': 'improving' if len(response_times) < 2 or response_times[-1] < response_times[-2] else 'degrading'
        }
        
    # Demonstration functions
    def demonstrate_sqa_activities(self):
        """Demonstrate all SQA activities"""
        print("\n=== Online Library System SQA Demonstration ===")
        
        # Demonstrate normal operations
        print("\n1. Performing library operations:")
        self.checkout_book('1001', '001')
        self.search_books('Python')
        self.return_book('1001', '001')
        
        # Demonstrate defect scenarios
        print("\n2. Demonstrating defect tracking:")
        self.checkout_book('9999', '001')  # Invalid user
        self.checkout_book('1001', '9999')  # Invalid book
        self.return_book('1001', '003')     # Book not checked out by this user
        
        # Generate reports
        print("\n3. Generating SQA Reports:")
        print("\nChange Control Report:")
        print(json.dumps(self.get_change_report(), indent=2))
        
        print("\nDefect Tracking Report:")
        print(json.dumps(self.get_defect_report(), indent=2))
        
        print("\nAudit Report:")
        print(json.dumps(self.get_audit_report(), indent=2))
        
        print("\nPerformance Report:")
        print(json.dumps(self.get_performance_report(), indent=2))
        
        print("\n=== Demonstration Complete ===")


# Main execution
if __name__ == "__main__":
    library_system = OnlineLibrarySystem()
    library_system.demonstrate_sqa_activities()
