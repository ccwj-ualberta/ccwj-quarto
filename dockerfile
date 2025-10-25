# Use rocker with RStudio Server and a specific R version
FROM rocker/r-ver:4.5.1

# Set environment variables
ENV RENV_VERSION=1.0.3

# Install system dependencies for spatial/data packages and more
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libxml2 \
    libgit2-dev \
    libudunits2-dev \
    libgdal-dev \
    libglpk-dev \
    wget \
    libfontconfig1-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Quarto CLI
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.7.32/quarto-1.7.32-linux-amd64.deb && \
    dpkg -i quarto-1.7.32-linux-amd64.deb && \
    rm quarto-1.7.32-linux-amd64.deb

# Create the rstudio user
RUN useradd -m rstudio

# Copy project files into container
WORKDIR /home/rstudio/project
COPY . /home/rstudio/project

# Ensure correct ownership and create the renv directory structure
RUN chown -R rstudio:rstudio /home/rstudio

# Install renv and restore packages from lockfile
USER rstudio

# Change to project directory
WORKDIR /home/rstudio/project

# Restore packages from lockfile
RUN R -e "install.packages('renv', repos = c(CRAN = 'https://cloud.r-project.org'))"
RUN R -e "renv::restore()"
