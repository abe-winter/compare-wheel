FROM python:3.9 AS build

ARG prefix
ARG repo
ARG branch

RUN git clone --branch $branch --depth 1 $repo
WORKDIR $prefix
RUN pip wheel --no-deps .

FROM scratch

ARG prefix
ARG whlname

COPY --from=build /$prefix/$whlname ./
