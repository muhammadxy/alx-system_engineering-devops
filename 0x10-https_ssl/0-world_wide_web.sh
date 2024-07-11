#!/bin/bash

# Function to query and extract DNS information
query_dns_info() {
    local subdomain="$1"
    local domain="$2"
    
    # Perform DNS query using dig, extract relevant information
    dig_output=$(dig +short "$subdomain.$domain" | awk '{ if (NR == 1) print $1, $2 }')
    
    # Determine record type and destination
    if [[ -n "$dig_output" ]]; then
        record_type=$(echo "$dig_output" | awk '{ print $2 }')
        destination=$(echo "$dig_output" | awk '{ print $1 }')
        echo "The subdomain $subdomain is a $record_type record and points to $destination"
    else
        echo "No information found for subdomain $subdomain"
    fi
}

# Main script logic
if [[ $# -lt 1 || $# -gt 2 ]]; then
    echo "Usage: $0 <domain> [<subdomain>]"
    exit 1
fi

domain="$1"

if [[ $# -eq 1 ]]; then
    # Query default subdomains
    query_dns_info "www" "$domain"
    query_dns_info "lb-01" "$domain"
    query_dns_info "web-01" "$domain"
    query_dns_info "web-02" "$domain"
else
    # Query specific subdomain
    subdomain="$2"
    query_dns_info "$subdomain" "$domain"
fi
