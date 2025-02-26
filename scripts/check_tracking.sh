#!/bin/bash

# Function to show usage
show_usage() {
    echo "Usage: $0 [tracking_id]"
    echo "If no tracking_id is provided, shows overall analytics"
}

# Show analytics
show_analytics() {
    curl -s http://localhost:8001/api/v1/tracking/analytics | \
    python3 -c "
import sys, json
data = json.load(sys.stdin)
print('\nEmail Analytics Summary:\n====================')
print(f'Total Sent: {data['total_sent']}')
print(f'Total Opened: {data['total_opened']}')
print(f'Total Clicked: {data['total_clicked']}')
print(f'Open Rate: {data['average_open_rate']*100:.1f}%')
print(f'Click Rate: {data['average_click_rate']*100:.1f}%')
print(f'Delivery Rate: {data['delivery_success_rate']*100:.1f}%')
"
}

# Show events for specific email
show_events() {
    local tracking_id=$1
    curl -s "http://localhost:8001/api/v1/tracking/events/$tracking_id" | \
    python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'\nEmail Tracking Events for {data['tracking_id']}:\n==================')
for e in data['events']:
    print(f'\nEvent: {e['event_type'].upper()}')
    print(f'Time: {e['timestamp']}')
    print(f'User Agent: {e['user_agent'] or 'N/A'}')
    print(f'IP: {e['ip_address'] or 'N/A'}')
    if e.get('metadata'):
        print('Metadata:')
        for k, v in e['metadata'].items():
            print(f'  {k}: {v}')
    print('-------------------')
"
}

# Main logic
if [ $# -eq 0 ]; then
    show_analytics
elif [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_usage
else
    show_events "$1"
fi 