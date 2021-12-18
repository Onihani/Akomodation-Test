// filter by region
async function show(region, pageNumber = 1) {
  console.log(region, pageNumber);

  try {
    const response = await fetch(
     `http://localhost:8000/region/?region=${region}&page=${pageNumber}`
    );

    const data = await response.json();

    const pageData = data.pop();
    console.log("pageItems", data);
    console.log("pageData", pageData);

    if (data.length === 0) {
      alert("Sorry are there no products in this page")
      return
    }

    const fetchedRegionsElem = document.createElement("div");
    fetchedRegionsElem.id = "fetched-regions";
    fetchedRegionsElem.classList.add("row");

    for (const property of data) {
      const propertyCol = document.createElement("div");
      propertyCol.classList.add("col-sm-6", "col-md-4", "col-lg-3", "text-center");

      const date = new Date(property.date);

      // <div class="col-sm-6 text-center">
      propertyCol.innerHTML = `
        <div class="property-desc-container shadow p-2 mb-3 bg-light" style="min-width: 12.5rem;">
          <!-- the properties displayed with their descriptions -->
          <div class="property-img-container mb-1">
            <a href="${property.url}" aria-label="${
        property.title
      }" tabindex="0">
              <img src="${
                property.image
              }" class="property-img" alt="property image">
            </a>
          </div>
          <h4>
            <a href="${property.url}" class="property-desc text-primary">${
        property.title
      }</a>
          </h4>
          <p class="font-weight-bold">Plan: ${property.plan}</p>
          <p style="margin: 0; padding: 0">
            Date posted ${date.toDateString()}, ${
        date.getHours() % 12
      }:${date.getMinutes()} ${date.getMinutes() >= 12 ? "pm" : "am"}.
          </p>
          <span class="lead">GH₵ ${property.price}</span>
          <h5>
            <svg class="svg-inline--fa fa-map-marker-alt fa-w-12" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="map-marker-alt" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" data-fa-i2svg=""><path fill="currentColor" d="M172.268 501.67C26.97 291.031 0 269.413 0 192 0 85.961 85.961 0 192 0s192 85.961 192 192c0 77.413-26.97 99.031-172.268 309.67-9.535 13.774-29.93 13.773-39.464 0zM192 272c44.183 0 80-35.817 80-80s-35.817-80-80-80-80 35.817-80 80 35.817 80 80 80z"></path></svg><!-- <i class="fas fa-map-marker-alt"></i> Font Awesome fontawesome.com -->${property.location}
          </h5>
          </div>
          `;
          // </div>

      fetchedRegionsElem.appendChild(propertyCol);
    }

    const fetchedRegionsPaginationElem = document.createElement("div");
    fetchedRegionsPaginationElem.id = "fetched-regions-pagination";
    fetchedRegionsPaginationElem.classList.add("w-100");

    let paginationItemsHtml = "";
    for (let i = 1; i <= pageData.pages; i++) {
      paginationItemsHtml += `<li class="page-item ${pageNumber == i ? 'active' : null}"><a class="page-link" onclick="show('${region}', ${i})">${i}</a></li>`;
    }

    const pagePaginationHtml = `
    <header class="w-100 d-flex justify-content-center">
      <nav aria-label="Page navigation" style="transform: translateX(-50%);">
        <ul class="pagination">
          <li class="page-item ${pageNumber == 1 ? 'disabled' : null}">
            <a class="page-link" onclick="show('${region}', ${pageNumber-1})" aria-label="Previous" role="button">
              <span aria-hidden="true">&laquo;</span>
            </a>
          </li>
          ${paginationItemsHtml}
          <li class="page-item ${pageNumber == pageData.pages ? 'disabled' : null}">
            <a class="page-link" onclick="show('${region}', ${pageNumber+1})" aria-label="Next" role="button" aria-disabled="true">
              <span aria-hidden="true">&raquo;</span>
            </a>
          </li>
        </ul>
      </nav>
    </header>
    `;

    fetchedRegionsPaginationElem.innerHTML = pagePaginationHtml;

    const fetchedProductsArea = document.querySelector(
      "#fetched-products-area"
    );

    if (document.querySelector("#fetched-regions")) {
      document
        .querySelector("#fetched-regions")
        .replaceWith(fetchedRegionsElem);
    } else {
      fetchedProductsArea.append(fetchedRegionsElem);
    }

    if (document.querySelector("#fetched-regions-pagination")) {
      document
        .querySelector("#fetched-regions-pagination")
        .replaceWith(fetchedRegionsPaginationElem);
    } else {
      fetchedProductsArea.append(fetchedRegionsPaginationElem);
    }
  } catch (error) {
    console.log("error", error);
  }

  document.querySelector(".text-box").value = region;
}
