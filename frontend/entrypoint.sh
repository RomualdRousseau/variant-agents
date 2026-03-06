#!/bin/sh

echo "Injecting runtime environment variables..."

# 1. Build a string of sed expressions
# Example: -e "s|PLACEHOLDER_A|valA|g" -e "s|PLACEHOLDER_B|valB|g"
SED_EXPR=""
for line in $(printenv | grep NEXT_PUBLIC_); do
  varname=$(echo "$line" | cut -d '=' -f 1)
  varvalue=$(echo "$line" | cut -d '=' -f 2)
  
  echo "Preparing replacement for $varname"
  SED_EXPR="${SED_EXPR} -e s|PLACEHOLDER_$varname|$varvalue|g"
done

# 2. Run find once and pass all files to sed at once using '+' 
# This uses the built-in multi-expression capability of sed
if [ -n "$SED_EXPR" ]; then
  find ./.next -type f -exec sed -i $SED_EXPR {} +
fi

echo "Injection complete."

# Continue to the main command
exec "$@"
