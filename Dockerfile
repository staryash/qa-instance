FROM daptin/daptin:travis
COPY schema/schema_chief_daptin.yaml /opt/daptin/schema_chief_daptin.yaml
COPY schema/initial_data.json /opt/daptin/initial_data.json
RUN mkdir -p /opt/daptin/gallery/images
RUN chmod 777 -R /opt/daptin/gallery/images
RUN mkdir -p /opt/daptin/gallery/audio
RUN chmod 777 /opt/daptin/gallery/audio
RUN ls -la
EXPOSE 5000
ENTRYPOINT ["/opt/daptin/daptin", "-runtime", "release", "-port", ":5000", "-db_type", "postgres",  "-db_connection_string", "host=production-postgres port=5432 user=qauser password=qauserpassword dbname=qa-daptin sslmode=disable"]