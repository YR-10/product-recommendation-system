const productGrid =
    document.getElementById("product-grid");

const recommendationGrid =
    document.getElementById(
        "recommendation-grid"
    );

const productCount =
    document.getElementById("product-count");

const searchInput =
    document.getElementById("search");

const heroSearch =
    document.getElementById("hero-search");

const sortSelect =
    document.getElementById("sort");

const productSection =
    document.getElementById("products");

const detailSection =
    document.getElementById(
        "product-detail"
    );

const detailContent =
    document.getElementById(
        "detail-content"
    );

const backButton =
    document.getElementById(
        "back-button"
    );

const categoryButtons =
    document.querySelectorAll(
        ".category-button"
    );


let products = [];

let activeCategory = "";


// =========================
// LOAD PRODUCTS
// =========================

async function loadProducts() {

    try {

        const response =
            await fetch("/products");

        if (!response.ok) {
            throw new Error(
                "Gagal mengambil produk."
            );
        }

        products =
            await response.json();

        productCount.textContent =
            `${products.length} produk tersedia`;

        const allButton =
            document.querySelector(
                '.category-button[data-category=""]'
            );

        if (allButton) {
            allButton.classList.add("active");
        }

        renderProducts(products);

    } catch (error) {

        console.error(error);

        productGrid.innerHTML = `
            <p>
                Gagal memuat produk.
            </p>
        `;
    }
}


// =========================
// FILTER + SORT
// =========================

function getFilteredProducts() {

    const keyword =
        searchInput.value
            .toLowerCase()
            .trim();

    let filtered =
        products.filter(product => {

            const matchesKeyword =
                product.nama
                    .toLowerCase()
                    .includes(keyword)

                ||

                product.brand
                    .toLowerCase()
                    .includes(keyword)

                ||

                product.kategori
                    .toLowerCase()
                    .includes(keyword)

                ||

                product.jenis
                    .toLowerCase()
                    .includes(keyword);

            const matchesCategory =
                !activeCategory
                ||
                product.kategori === activeCategory;

            return (
                matchesKeyword
                &&
                matchesCategory
            );
        });


    // =========================
    // SORT
    // =========================

    switch (sortSelect.value) {

        case "price-low":

            filtered.sort(
                (a, b) =>
                    a.harga - b.harga
            );

            break;


        case "price-high":

            filtered.sort(
                (a, b) =>
                    b.harga - a.harga
            );

            break;


        case "name-az":

            filtered.sort(
                (a, b) =>
                    a.nama.localeCompare(
                        b.nama,
                        "id"
                    )
            );

            break;


        case "name-za":

            filtered.sort(
                (a, b) =>
                    b.nama.localeCompare(
                        a.nama,
                        "id"
                    )
            );

            break;
    }

    return filtered;
}


function applyFilters() {

    const filtered =
        getFilteredProducts();

    renderProducts(filtered);

    productCount.textContent =
        `${filtered.length} produk ditemukan`;
}


// =========================
// RENDER PRODUCTS
// =========================

function renderProducts(
    productList
) {

    productGrid.innerHTML = "";

    if (productList.length === 0) {

        productGrid.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">
                    🔎
                </div>

                <h3>
                    Produk tidak ditemukan
                </h3>

                <p>
                    Coba kata kunci atau kategori lain.
                </p>
            </div>
        `;

        return;
    }


    productList.forEach(product => {

        const card =
            document.createElement("div");

        card.className =
            "product-card";

        card.innerHTML = `
            <div class="product-type">
                ${escapeHtml(product.kategori)}
            </div>

            <h3>
                ${escapeHtml(product.nama)}
            </h3>

            <div class="product-brand">
                ${escapeHtml(product.brand)}
            </div>

            <div class="product-price">
                ${formatPrice(product.harga)}
            </div>
        `;

        card.addEventListener(
            "click",
            () => openProduct(product.id)
        );

        productGrid.appendChild(card);
    });
}


// =========================
// OPEN PRODUCT
// =========================

async function openProduct(
    productId
) {

    try {

        const product =
            products.find(
                item => item.id === productId
            );

        if (!product) {
            throw new Error(
                "Produk tidak ditemukan."
            );
        }


        productSection.classList.add(
            "hidden"
        );

        detailSection.classList.remove(
            "hidden"
        );


        renderProductDetail(product);


        recommendationGrid.innerHTML = `
            <p>
                Memuat rekomendasi...
            </p>
        `;


        const response =
            await fetch(
                `/products/${productId}/recommendations?top_n=3`
            );


        if (!response.ok) {

            throw new Error(
                "Gagal mengambil rekomendasi."
            );
        }


        const data =
            await response.json();


        renderRecommendations(
            data.recommendations
        );


        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    } catch (error) {

        console.error(error);

        recommendationGrid.innerHTML = `
            <div class="empty-state">
                <h3>
                    Gagal memuat rekomendasi
                </h3>
            </div>
        `;
    }
}


// =========================
// PRODUCT DETAIL
// =========================

function renderProductDetail(
    product
) {

    detailContent.innerHTML = `
        <div class="product-type">
            ${escapeHtml(product.kategori)}
        </div>

        <h1>
            ${escapeHtml(product.nama)}
        </h1>

        <p class="product-brand">
            ${escapeHtml(product.brand)}
        </p>

        <p class="product-price">
            ${formatPrice(product.harga)}
        </p>

        <p class="detail-description">
            ${escapeHtml(product.deskripsi)}
        </p>

        <div class="specifications">

            <div class="spec-item">
                <span class="spec-label">
                    Jenis
                </span>

                ${escapeHtml(product.jenis)}
            </div>

            <div class="spec-item">
                <span class="spec-label">
                    Kategori
                </span>

                ${escapeHtml(product.kategori)}
            </div>

            <div class="spec-item">
                <span class="spec-label">
                    RAM
                </span>

                ${formatSpecification(
                    product.ram_gb,
                    "GB"
                )}
            </div>

            <div class="spec-item">
                <span class="spec-label">
                    Storage
                </span>

                ${formatSpecification(
                    product.storage_gb,
                    "GB"
                )}
            </div>

        </div>
    `;
}


// =========================
// RECOMMENDATIONS
// =========================

function renderRecommendations(
    recommendations
) {

    recommendationGrid.innerHTML = "";


    if (
        recommendations.length === 0
    ) {

        recommendationGrid.innerHTML = `
            <div class="empty-state">
                <h3>
                    Belum ada rekomendasi
                </h3>
            </div>
        `;

        return;
    }


    recommendations.forEach(
        recommendation => {

            const card =
                document.createElement("div");


            card.className =
                "product-card";


            card.innerHTML = `
                <div class="product-type">
                    ${escapeHtml(
                        recommendation.kategori
                    )}
                </div>

                <h3>
                    ${escapeHtml(
                        recommendation.nama
                    )}
                </h3>

                <div class="product-brand">
                    ${escapeHtml(
                        recommendation.brand
                    )}
                </div>

                <div class="product-price">
                    ${formatPrice(
                        recommendation.harga
                    )}
                </div>

                <div class="similarity">
                    Kemiripan:
                    ${(recommendation.similarity * 100).toFixed(1)}%
                </div>

                <div class="recommendation-reasons">

                    <div class="reason-title">
                        Mengapa direkomendasikan?
                    </div>

                    ${
                        recommendation.reasons
                            .map(reason => `
                                <div class="reason-item">
                                    ✓ ${escapeHtml(reason)}
                                </div>
                            `)
                            .join("")
                    }

                </div>
            `;


            card.addEventListener(
                "click",
                () => openProduct(
                    recommendation.id
                )
            );


            recommendationGrid.appendChild(
                card
            );
        }
    );
}


// =========================
// SEARCH
// =========================

searchInput.addEventListener(
    "input",
    applyFilters
);


heroSearch.addEventListener(
    "input",
    event => {

        searchInput.value =
            event.target.value;

        applyFilters();

        document
            .getElementById("products")
            .scrollIntoView({
                behavior: "smooth"
            });
    }
);


// =========================
// SORT
// =========================

sortSelect.addEventListener(
    "change",
    applyFilters
);


// =========================
// CATEGORY
// =========================

categoryButtons.forEach(
    button => {

        button.addEventListener(
            "click",
            () => {

                categoryButtons.forEach(
                    item =>
                        item.classList.remove(
                            "active"
                        )
                );


                button.classList.add(
                    "active"
                );


                activeCategory =
                    button.dataset.category;


                applyFilters();
            }
        );
    }
);


// =========================
// BACK
// =========================

backButton.addEventListener(
    "click",
    () => {

        detailSection.classList.add(
            "hidden"
        );

        productSection.classList.remove(
            "hidden"
        );

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }
);


// =========================
// FORMAT PRICE
// =========================

function formatPrice(
    price
) {

    return new Intl.NumberFormat(
        "id-ID",
        {
            style: "currency",
            currency: "IDR",
            maximumFractionDigits: 0
        }
    ).format(price);
}


// =========================
// FORMAT SPECIFICATION
// =========================

function formatSpecification(
    value,
    unit
) {

    if (
        value === null ||
        value === undefined
    ) {
        return "Tidak tersedia";
    }

    return `${value} ${unit}`;
}


// =========================
// SECURITY
// =========================

function escapeHtml(
    value
) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


// =========================
// START APP
// =========================

loadProducts();