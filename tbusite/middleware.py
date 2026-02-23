"""
Middleware to add custom CSS to UNFOLD admin pages.
"""
from django.utils.deprecation import MiddlewareMixin


class AdminCustomCSSMiddleware(MiddlewareMixin):
    """
    Middleware that adds custom CSS to all admin pages for visible input borders.
    """
    
    CSS = '''
    <style>
        .w-full[type="text"], 
        .w-full[type="email"], 
        .w-full[type="password"], 
        .w-full[type="number"], 
        .w-full[type="url"], 
        .w-full[type="tel"], 
        .w-full[type="search"], 
        input[type="text"], 
        input[type="email"], 
        input[type="password"], 
        input[type="number"], 
        input[type="url"], 
        input[type="tel"], 
        input[type="search"], 
        textarea, 
        select { 
            border: 1px solid #d1d5db !important; 
            border-radius: 4px !important; 
            padding: 8px 12px !important; 
            background-color: #fff !important; 
        }
        .w-full:focus, 
        input:focus, 
        textarea:focus, 
        select:focus { 
            border-color: #4f46e5 !important; 
            outline: 2px solid #4f46e5 !important; 
            outline-offset: 1px !important; 
        }
        .w-full:hover, 
        input:hover, 
        textarea:hover, 
        select:hover { 
            border-color: #9ca3af !important; 
        }
        .w-full:disabled,
        input:disabled, 
        textarea:disabled, 
        select:disabled { 
            background-color: #f3f4f6 !important; 
            border-color: #e5e7eb !important; 
        }
    </style>
    '''
    
    def process_response(self, request, response):
        # Only apply to admin pages
        if request.path.startswith('/admin/') and response.status_code == 200:
            # Add CSS before </head>
            if b'</head>' in response.content:
                response.content = response.content.replace(
                    b'</head>',
                    (self.CSS + '</head>').encode('utf-8')
                )
        return response
