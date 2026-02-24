/**
 * AI Content Generator Widget JavaScript
 * 
 * This module handles the AI content generation functionality in Django admin.
 */

(function() {
    'use strict';

    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        initAIWidgets();
    });

    // Also initialize on Django admin inline additions
    if (typeof django !== 'undefined' && django.jQuery) {
        django.jQuery(document).on('formset:added', function(event, $row, formsetName) {
            initAIWidgets($row[0]);
        });
    }

    function initAIWidgets(container) {
        container = container || document;
        const buttons = container.querySelectorAll('.ai-generate-btn');
        
        buttons.forEach(function(button) {
            if (!button.dataset.initialized) {
                button.addEventListener('click', handleAIGenerate);
                button.dataset.initialized = 'true';
            }
        });
    }

    function handleAIGenerate(event) {
        event.preventDefault();
        
        const button = event.currentTarget;
        const widget = button.closest('.ai-textarea-widget');
        const textarea = widget.querySelector('textarea');
        const btnText = button.querySelector('.ai-btn-text');
        const btnLoading = button.querySelector('.ai-btn-loading');
        const statusSpan = widget.querySelector('.ai-status');

        // Get context data from related fields
        const contextFields = button.dataset.contextFields.split(',').filter(f => f);
        const contextData = {};

        contextFields.forEach(function(fieldName) {
            const field = findFieldByName(fieldName, widget);
            if (field) {
                contextData[fieldName] = field.value;
            }
        });

        // Show loading state
        button.disabled = true;
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline-flex';
        hideStatus(statusSpan);

        // Prepare request data
        const requestData = {
            prompt_type: button.dataset.prompt,
            context: contextData,
            field_name: textarea.name
        };

        // Make API request
        fetch('/admin/ai/generate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify(requestData)
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            if (data.success) {
                textarea.value = data.content;
                showStatus(statusSpan, 'Content generated successfully!', 'success');
                
                // Trigger change event for any listeners
                textarea.dispatchEvent(new Event('change', { bubbles: true }));
            } else {
                showStatus(statusSpan, data.error || 'Failed to generate content', 'error');
            }
        })
        .catch(function(error) {
            showStatus(statusSpan, 'Request failed: ' + error.message, 'error');
        })
        .finally(function() {
            // Reset button state
            button.disabled = false;
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
        });
    }

    function findFieldByName(fieldName, widget) {
        // Try to find field in the same form
        const form = widget.closest('form');
        if (!form) return null;

        // Try various field name patterns used in Django admin
        const patterns = [
            fieldName,
            `id_${fieldName}`,
            `id_${fieldName}_0`,
        ];

        // Also try with form prefixes (for inlines)
        const textareaName = widget.querySelector('textarea').name;
        if (textareaName) {
            const match = textareaName.match(/^(.+)-\d+-/);
            if (match) {
                patterns.push(`${match[1]}-${fieldName}`);
                patterns.push(`id_${match[1]}-${fieldName}`);
            }
        }

        for (const pattern of patterns) {
            // Try by ID
            let field = document.getElementById(pattern);
            if (field) return field;

            // Try by name
            field = form.querySelector(`[name="${pattern}"]`);
            if (field) return field;

            // Try by name ending with the field name
            field = form.querySelector(`[name$="-${fieldName}"]`);
            if (field) return field;
        }

        return null;
    }

    function getCSRFToken() {
        // Try to get CSRF token from cookie
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }

        // Try to get from form input
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (csrfInput) {
            return csrfInput.value;
        }

        return '';
    }

    function showStatus(element, message, type) {
        if (!element) return;
        
        element.textContent = message;
        element.className = 'ai-status ' + type;
        element.style.display = 'inline-block';

        // Auto-hide success messages after 5 seconds
        if (type === 'success') {
            setTimeout(function() {
                hideStatus(element);
            }, 5000);
        }
    }

    function hideStatus(element) {
        if (!element) return;
        element.style.display = 'none';
        element.textContent = '';
        element.className = 'ai-status';
    }

    // Expose for external use if needed
    window.AIContentGenerator = {
        init: initAIWidgets,
        generate: handleAIGenerate
    };

})();
