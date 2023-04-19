FROM python:3.10

# Copy all files
COPY . .

# install deps
RUN pip install --upgrade pip && \
    pip install --upgrade poetry


# install dependencies
RUN make install


CMD ["make", "migrate-and-run"]