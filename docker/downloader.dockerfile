FROM golang:1.17.0 AS builder
RUN mkdir /app
WORKDIR /app
COPY downloader ./downloader
WORKDIR /app/downloader
RUN CGO_ENABLED=0 GOOS=linux go build -o main

FROM alpine:latest AS production
WORKDIR /app
COPY --from=builder /app .
WORKDIR /app/downloader
CMD ["./main"]