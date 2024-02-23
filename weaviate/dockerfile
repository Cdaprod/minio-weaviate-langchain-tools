# Use the official Weaviate image
FROM semitechnologies/weaviate:latest

# Copy schema.json and entrypoint.sh into the container
COPY schema.json /weaviate/schema.json
COPY entrypoint.sh /weaviate/entrypoint.sh

# Make the script executable
RUN chmod +x /weaviate/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/weaviate/entrypoint.sh"]