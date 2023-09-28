#!/bin/bash
# Test the trivial web server.
# Usage:  ./tests.sh localhost:<port-num>
# Example: tests.sh localhost:5000

# Check if URL base argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <base_url>"
    echo "Example: $0 localhost:5000"
    exit 1
fi

URLbase=$1

# Test cases for the body
function expect_body() {
    local path=$1
    local expect=$2
    local response=$(curl --silent "${URLbase}/${path}")

    if echo "$response" | grep -q "${expect}" ; then
      echo "Pass -- found ${expect} in ${path}"
    else
      echo "*** FAIL *** expecting ${expect} in ${URLbase}/${path}"
    fi
}

# Test case for the status
function expect_status() {
    local path=$1
    local expect=$2
    local status=$(curl --silent -o /dev/null -w '%{http_code}' "${URLbase}/${path}")

    if [ "$status" == "$expect" ]; then
      echo "Pass -- found status ${expect} for ${path}"
    else
      echo "*** FAIL *** expecting status ${expect} for ${URLbase}/${path}, got ${status}"
    fi
}

# Original tests
expect_body trivia.html "Seriously?"
expect_status trivia.html "200"
expect_status nosuch.html "404"
expect_status there/theybe.html "404"
expect_status there//theybe.html "403"

# Additional tests

# Testing .css files
expect_status style.css "200"
expect_status nonexistent.css "404"

# Testing forbidden patterns
expect_status ~/forbidden.html "403"
expect_status ../forbidden.html "403"

# Testing root access
expect_status "" "404"  # Assuming the server returns 404 for the root

