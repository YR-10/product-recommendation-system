// =========================
// TOKEN
// =========================

const TOKEN_KEY =
    "productrec_access_token";


// =========================
// DOM ELEMENTS
// =========================

// Navigation
const navItems =
    document.querySelectorAll(
        ".admin-nav-item"
    );

const dashboardSection =
    document.getElementById(
        "section-dashboard"
    );

const productsSection =
    document.getElementById(
        "section-products"
    );

const usersSection =
    document.getElementById(
        "section-users"
    );

const pageTitle =
    document.getElementById(
        "page-title"
    );


// Header profile
const adminUser =
    document.getElementById(
        "admin-user"
    );

const adminProfileMenu =
    document.getElementById(
        "admin-profile-menu"
    );

const adminMenuUsername =
    document.getElementById(
        "admin-menu-username"
    );

const adminMenuEmail =
    document.getElementById(
        "admin-menu-email"
    );

const adminMenuLogout =
    document.getElementById(
        "admin-menu-logout"
    );


// Dashboard
const totalProducts =
    document.getElementById(
        "total-products"
    );

const totalCategories =
    document.getElementById(
        "total-categories"
    );

    const totalUsers =
    document.getElementById(
        "total-users"
    );

const userTableContainer =
    document.getElementById(
        "user-table-container"
    );


// Product management
const addProductButton =
    document.getElementById(
        "add-product-button"
    );

const productTableContainer =
    document.getElementById(
        "product-table-container"
    );

const productPagination =
    document.getElementById(
        "product-pagination"
    );

const adminProductSearch =
    document.getElementById(
        "admin-product-search"
    );

const adminCategoryFilter =
    document.getElementById(
        "admin-category-filter"
    );


// Product modal
const productModal =
    document.getElementById(
        "product-modal"
    );

const productModalClose =
    document.getElementById(
        "product-modal-close"
    );

const productModalTitle =
    document.getElementById(
        "product-modal-title"
    );

const productForm =
    document.getElementById(
        "product-form"
    );

const productIdInput =
    document.getElementById(
        "product-id"
    );

const productNameInput =
    document.getElementById(
        "product-name"
    );

const productBrandInput =
    document.getElementById(
        "product-brand"
    );

const productTypeInput =
    document.getElementById(
        "product-type"
    );

const productCategoryInput =
    document.getElementById(
        "product-category"
    );

const productDescriptionInput =
    document.getElementById(
        "product-description"
    );

const productRamInput =
    document.getElementById(
        "product-ram"
    );

const productStorageInput =
    document.getElementById(
        "product-storage"
    );

const productPriceInput =
    document.getElementById(
        "product-price"
    );

const productFormMessage =
    document.getElementById(
        "product-form-message"
    );

const productSubmitButton =
    document.getElementById(
        "product-submit-button"
    );


// Admin logout from sidebar
const adminLogout =
    document.getElementById(
        "admin-logout"
    );


// =========================
// STATE
// =========================

let allAdminProducts = [];

let currentProductPage = 1;

const productsPerPage = 10;


// =========================
// AUTH / API
// =========================

async function adminRequest(
    url,
    options = {}
) {

    const token =
        sessionStorage.getItem(
            TOKEN_KEY
        );


    if (!token) {

        window.location.href =
            "/";

        return null;
    }


    const headers = {
        ...(options.headers || {}),
        Authorization:
            `Bearer ${token}`
    };


    const response =
        await fetch(
            url,
            {
                ...options,
                headers
            }
        );


    if (
        response.status === 401 ||
        response.status === 403
    ) {

        sessionStorage.removeItem(
            TOKEN_KEY
        );

        window.location.href =
            "/";

        return null;
    }


    return response;
}


// =========================
// CURRENT ADMIN
// =========================

async function loadCurrentAdmin() {

    const response =
        await adminRequest(
            "/auth/me"
        );


    if (!response) {
        return false;
    }


    const user =
        await response.json();


    if (user.role !== "admin") {

        sessionStorage.removeItem(
            TOKEN_KEY
        );

        window.location.href =
            "/";

        return false;
    }


    if (adminUser) {

        adminUser.textContent =
            `👤 ${user.username}`;
    }


    if (adminMenuUsername) {

        adminMenuUsername.textContent =
            user.username;
    }


    if (adminMenuEmail) {

        adminMenuEmail.textContent =
            user.email;
    }


    return true;
}


// =========================
// LOAD PRODUCTS
// =========================

async function loadProducts() {

    const response =
        await adminRequest(
            "/admin/products"
        );


    if (!response) {
        return;
    }


    const data =
        await response.json();


    allAdminProducts =
        Array.isArray(
            data.products
        )
            ? data.products
            : [];


    currentProductPage = 1;


    if (totalProducts) {

        totalProducts.textContent =
            allAdminProducts.length;
    }


    renderProducts(
        getFilteredAdminProducts()
    );
}


// =========================
// LOAD CATEGORIES
// =========================

async function loadCategories() {

    const response =
        await adminRequest(
            "/admin/categories"
        );


    if (!response) {
        return;
    }


    const data =
        await response.json();


    const categories =
        Array.isArray(
            data.categories
        )
            ? data.categories
            : [];


    if (totalCategories) {

        totalCategories.textContent =
            categories.length;
    }


    populateCategoryFilter(
        categories
    );

    populateProductCategory(
        categories
    );
}

// =========================
// LOAD USERS
// =========================

async function loadUsers() {

    const response =
        await adminRequest(
            "/admin/users"
        );


    if (!response) {
        return;
    }


    const data =
        await response.json();


    const users =
        Array.isArray(
            data.users
        )
            ? data.users
            : [];


    if (totalUsers) {

        totalUsers.textContent =
            users.length;
    }


    renderUsers(
        users
    );
}

// =========================
// CATEGORY FILTER
// =========================

function populateCategoryFilter(
    categories
) {

    if (!adminCategoryFilter) {
        return;
    }


    const currentValue =
        adminCategoryFilter.value;


    adminCategoryFilter.innerHTML = `
        <option value="">
            Semua kategori
        </option>
    `;


    categories.forEach(
        category => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                category.nama;


            option.textContent =
                category.nama;


            adminCategoryFilter.appendChild(
                option
            );
        }
    );


    if (
        categories.some(
            category =>
                category.nama ===
                currentValue
        )
    ) {

        adminCategoryFilter.value =
            currentValue;
    }
}


// =========================
// PRODUCT CATEGORY
// =========================

function populateProductCategory(
    categories
) {

    if (!productCategoryInput) {
        return;
    }


    productCategoryInput.innerHTML =
        "";


    categories.forEach(
        category => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                category.id;


            option.textContent =
                category.nama;


            productCategoryInput.appendChild(
                option
            );
        }
    );
}


// =========================
// FILTER PRODUCTS
// =========================

function getFilteredAdminProducts() {

    const keyword =
        adminProductSearch
            ? adminProductSearch.value
                .toLowerCase()
                .trim()
            : "";


    const category =
        adminCategoryFilter
            ? adminCategoryFilter.value
            : "";


    return allAdminProducts.filter(
        product => {

            const matchesKeyword =
                !keyword ||
                String(
                    product.nama || ""
                )
                    .toLowerCase()
                    .includes(
                        keyword
                    ) ||
                String(
                    product.brand || ""
                )
                    .toLowerCase()
                    .includes(
                        keyword
                    ) ||
                String(
                    product.jenis || ""
                )
                    .toLowerCase()
                    .includes(
                        keyword
                    );


            const matchesCategory =
                !category ||
                product.kategori ===
                    category;


            return (
                matchesKeyword &&
                matchesCategory
            );
        }
    );
}


function applyAdminProductFilters() {

    currentProductPage = 1;


    renderProducts(
        getFilteredAdminProducts()
    );
}

// =========================
// RENDER USERS
// =========================

function renderUsers(
    users
) {

    if (!userTableContainer) {
        return;
    }


    if (!users.length) {

        userTableContainer.innerHTML = `
            <p class="loading-text">
                Belum ada user.
            </p>
        `;

        return;
    }


    userTableContainer.innerHTML = `

        <div class="admin-table-wrapper">

            <table class="admin-table">

                <thead>

                    <tr>

                        <th>ID</th>

                        <th>Username</th>

                        <th>Email</th>

                        <th>Role</th>

                    </tr>

                </thead>


                <tbody>

                    ${users.map(
                        user => `

                            <tr>

                                <td>
                                    ${user.id}
                                </td>

                                <td>
                                    ${escapeHtml(
                                        user.username
                                    )}
                                </td>

                                <td>
                                    ${escapeHtml(
                                        user.email
                                    )}
                                </td>

                                <td>

                                    <span
                                        class="role-badge ${
                                            user.role ===
                                            "admin"
                                                ? "role-admin"
                                                : "role-user"
                                        }"
                                    >
                                        ${escapeHtml(
                                            user.role
                                        )}
                                    </span>

                                </td>

                            </tr>

                        `
                    ).join("")}

                </tbody>

            </table>

        </div>
    `;
}

// =========================
// RENDER PRODUCTS
// =========================

function renderProducts(
    products
) {

    if (!productTableContainer) {
        return;
    }


    const totalPages =
        Math.max(
            1,
            Math.ceil(
                products.length /
                productsPerPage
            )
        );


    if (
        currentProductPage >
        totalPages
    ) {

        currentProductPage =
            totalPages;
    }


    const startIndex =
        (
            currentProductPage - 1
        ) *
        productsPerPage;


    const endIndex =
        startIndex +
        productsPerPage;


    const pageProducts =
        products.slice(
            startIndex,
            endIndex
        );


    // =========================
    // EMPTY
    // =========================

    if (!products.length) {

        productTableContainer.innerHTML = `
            <p class="loading-text">
                Tidak ada produk yang ditemukan.
            </p>
        `;


        renderPagination(
            0,
            1
        );

        return;
    }


    // =========================
    // TABLE
    // =========================

    productTableContainer.innerHTML = `

        <div class="admin-table-wrapper">

            <table class="admin-table">

                <thead>

                    <tr>

                        <th>ID</th>

                        <th>Produk</th>

                        <th>Brand</th>

                        <th>Kategori</th>

                        <th>Harga</th>

                        <th>Actions</th>

                    </tr>

                </thead>


                <tbody>

                    ${pageProducts.map(
                        product => `

                            <tr>

                                <td>
                                    ${product.id}
                                </td>


                                <td>
                                    ${escapeHtml(
                                        product.nama
                                    )}
                                </td>


                                <td>
                                    ${escapeHtml(
                                        product.brand
                                    )}
                                </td>


                                <td>
                                    ${escapeHtml(
                                        product.kategori || "-"
                                    )}
                                </td>


                                <td>
                                    ${formatPrice(
                                        product.harga
                                    )}
                                </td>


                                <td>

                                    <div class="table-actions">

                                        <button
                                            class="edit-product-button"
                                            data-id="${product.id}"
                                            type="button"
                                        >
                                            Edit
                                        </button>


                                        <button
                                            class="delete-product-button"
                                            data-id="${product.id}"
                                            type="button"
                                        >
                                            Delete
                                        </button>

                                    </div>

                                </td>

                            </tr>

                        `
                    ).join("")}

                </tbody>

            </table>

        </div>
    `;


    // =========================
    // TABLE EVENT DELEGATION
    // =========================

    const table =
        productTableContainer.querySelector(
            ".admin-table"
        );


    if (table) {

        table.addEventListener(
            "click",
            async event => {

                const button =
                    event.target.closest(
                        "button"
                    );


                if (!button) {
                    return;
                }


                event.preventDefault();

                event.stopPropagation();


                const productId =
                    Number(
                        button.dataset.id
                    );


                if (
                    button.classList.contains(
                        "edit-product-button"
                    )
                ) {

                    const product =
                        allAdminProducts.find(
                            item =>
                                Number(
                                    item.id
                                ) ===
                                productId
                        );


                    if (product) {

                        await openEditProductModal(
                            product
                        );
                    }


                    return;
                }


                if (
                    button.classList.contains(
                        "delete-product-button"
                    )
                ) {

                    await deleteProduct(
                        productId
                    );
                }
            }
        );
    }


    renderPagination(
        products.length,
        totalPages,
        startIndex,
        endIndex
    );
}


// =========================
// PAGINATION
// =========================

function renderPagination(
    totalItems,
    totalPages,
    startIndex = 0,
    endIndex = 0
) {

    if (!productPagination) {
        return;
    }


    if (!totalItems) {

        productPagination.innerHTML =
            "";

        return;
    }


    const start =
        startIndex + 1;


    const end =
        Math.min(
            endIndex,
            totalItems
        );


    let pages = "";


    for (
        let page = 1;
        page <= totalPages;
        page++
    ) {

        pages += `

            <button
                class="pagination-button ${
                    page ===
                    currentProductPage
                        ? "active"
                        : ""
                }"
                data-page="${page}"
                type="button"
            >
                ${page}
            </button>

        `;
    }


    productPagination.innerHTML = `

        <div class="pagination-info">

            Menampilkan
            ${start}
            -
            ${end}
            dari
            ${totalItems}
            produk

        </div>


        <div class="pagination-buttons">

            <button
                class="pagination-button"
                data-page="prev"
                type="button"
                ${
                    currentProductPage === 1
                        ? "disabled"
                        : ""
                }
            >
                ←
            </button>


            ${pages}


            <button
                class="pagination-button"
                data-page="next"
                type="button"
                ${
                    currentProductPage === totalPages
                        ? "disabled"
                        : ""
                }
            >
                →
            </button>

        </div>
    `;


    productPagination
        .querySelectorAll(
            ".pagination-button"
        )
        .forEach(
            button => {

                button.addEventListener(
                    "click",
                    () => {

                        const action =
                            button.dataset.page;


                        if (
                            action ===
                            "prev"
                        ) {

                            if (
                                currentProductPage >
                                1
                            ) {

                                currentProductPage--;
                            }
                        }


                        else if (
                            action ===
                            "next"
                        ) {

                            if (
                                currentProductPage <
                                totalPages
                            ) {

                                currentProductPage++;
                            }
                        }


                        else {

                            currentProductPage =
                                Number(
                                    action
                                );
                        }


                        renderProducts(
                            getFilteredAdminProducts()
                        );
                    }
                );
            }
        );
}


// =========================
// PRODUCT MODAL
// =========================

async function openCreateProductModal() {

    if (!productModal) {
        return;
    }


    productForm.reset();


    productIdInput.value =
        "";


    productModalTitle.textContent =
        "Tambah Produk";


    productSubmitButton.textContent =
        "Simpan Produk";


    productFormMessage.textContent =
        "";


    productModal.classList.remove(
        "hidden"
    );
}


function closeProductModal() {

    if (!productModal) {
        return;
    }


    productModal.classList.add(
        "hidden"
    );
}


async function openEditProductModal(
    product
) {

    if (!productModal) {
        return;
    }


    productModalTitle.textContent =
        "Edit Produk";


    productSubmitButton.textContent =
        "Simpan Perubahan";


    productIdInput.value =
        product.id;


    productNameInput.value =
        product.nama || "";


    productBrandInput.value =
        product.brand || "";


    productTypeInput.value =
        product.jenis || "";


    productDescriptionInput.value =
        product.deskripsi || "";


    productRamInput.value =
        product.ram_gb ?? "";


    productStorageInput.value =
        product.storage_gb ?? "";


    productPriceInput.value =
        product.harga ?? "";


    // Pastikan kategori sudah terisi
    if (
        !productCategoryInput.options.length
    ) {

        await loadCategories();
    }


    const categoryOption =
        [...productCategoryInput.options]
            .find(
                option =>
                    option.textContent.trim() ===
                    String(
                        product.kategori || ""
                    ).trim()
            );


    if (categoryOption) {

        productCategoryInput.value =
            categoryOption.value;
    }


    productFormMessage.textContent =
        "";


    productModal.classList.remove(
        "hidden"
    );
}


// =========================
// SAVE PRODUCT
// =========================

if (productForm) {

    productForm.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            if (productFormMessage) {

                productFormMessage.textContent =
                    "Menyimpan...";
            }


            try {

                const productId =
                    productIdInput.value.trim();


                const payload = {

                    nama:
                        productNameInput.value.trim(),

                    brand:
                        productBrandInput.value.trim(),

                    jenis:
                        productTypeInput.value.trim(),

                    kategori_id:
                        Number(
                            productCategoryInput.value
                        ),

                    deskripsi:
                        productDescriptionInput.value.trim(),

                    ram_gb:
                        productRamInput.value
                            ? Number(
                                productRamInput.value
                            )
                            : null,

                    storage_gb:
                        productStorageInput.value
                            ? Number(
                                productStorageInput.value
                            )
                            : null,

                    harga:
                        Number(
                            productPriceInput.value
                        )
                };


                const method =
                    productId
                        ? "PUT"
                        : "POST";


                const url =
                    productId
                        ? `/admin/products/${productId}`
                        : "/admin/products";


                const response =
                    await adminRequest(
                        url,
                        {
                            method,

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    payload
                                )
                        }
                    );


                if (!response) {
                    return;
                }


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "Gagal menyimpan produk."
                    );
                }


                closeProductModal();


                await loadProducts();

                await loadCategories();


                showSection(
                    "products"
                );


            } catch (error) {

                console.error(
                    "Save product error:",
                    error
                );


                if (productFormMessage) {

                    productFormMessage.textContent =
                        error.message ||
                        "Gagal menyimpan produk.";
                }
            }
        }
    );
}


// =========================
// DELETE PRODUCT
// =========================

async function deleteProduct(
    productId
) {

    const product =
        allAdminProducts.find(
            item =>
                Number(item.id) ===
                Number(productId)
        );


    const productName =
        product
            ? product.nama
            : "produk ini";


    const confirmed =
        window.confirm(
            `Yakin ingin menghapus ${productName}?`
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await adminRequest(
                `/admin/products/${productId}`,
                {
                    method: "DELETE"
                }
            );


        if (!response) {
            return;
        }


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Gagal menghapus produk."
            );
        }


        await loadProducts();


    } catch (error) {

        console.error(
            "Delete product error:",
            error
        );


        alert(
            error.message ||
            "Gagal menghapus produk."
        );
    }
}


// =========================
// ADD PRODUCT BUTTON
// =========================

if (addProductButton) {

    addProductButton.addEventListener(
        "click",
        openCreateProductModal
    );
}


// =========================
// CLOSE PRODUCT MODAL
// =========================

if (productModalClose) {

    productModalClose.addEventListener(
        "click",
        closeProductModal
    );
}


// =========================
// SEARCH
// =========================

if (adminProductSearch) {

    adminProductSearch.addEventListener(
        "input",
        applyAdminProductFilters
    );
}


// =========================
// CATEGORY FILTER
// =========================

if (adminCategoryFilter) {

    adminCategoryFilter.addEventListener(
        "change",
        applyAdminProductFilters
    );
}


// =========================
// NAVIGATION
// =========================

function showSection(
    section
) {

    if (dashboardSection) {

        dashboardSection.classList.add(
            "hidden"
        );
    }


    if (productsSection) {

        productsSection.classList.add(
            "hidden"
        );
    }


    if (usersSection) {

        usersSection.classList.add(
            "hidden"
        );
    }


    navItems.forEach(
        item =>
            item.classList.remove(
                "active"
            )
    );


    const activeNav =
        document.querySelector(
            `[data-section="${section}"]`
        );


    if (activeNav) {

        activeNav.classList.add(
            "active"
        );
    }


    if (section === "dashboard") {

        if (dashboardSection) {

            dashboardSection.classList.remove(
                "hidden"
            );
        }


        if (pageTitle) {

            pageTitle.textContent =
                "Dashboard";
        }
    }


    if (section === "products") {

        if (productsSection) {

            productsSection.classList.remove(
                "hidden"
            );
        }


        if (pageTitle) {

            pageTitle.textContent =
                "Products";
        }
    }


    if (section === "users") {

        if (usersSection) {

            usersSection.classList.remove(
                "hidden"
            );
        }


        if (pageTitle) {

            pageTitle.textContent =
                "Users";
        }
    }
}


navItems.forEach(
    item => {

        item.addEventListener(
            "click",
            () => {

                showSection(
                    item.dataset.section
                );
            }
        );
    }
);


// =========================
// ADMIN PROFILE DROPDOWN
// =========================

if (adminUser) {

    adminUser.addEventListener(
        "click",
        event => {

            event.preventDefault();

            event.stopPropagation();


            if (adminProfileMenu) {

                adminProfileMenu.classList.toggle(
                    "hidden"
                );
            }
        }
    );
}


document.addEventListener(
    "click",
    event => {

        if (
            adminProfileMenu &&
            adminUser &&
            !adminProfileMenu.contains(
                event.target
            ) &&
            !adminUser.contains(
                event.target
            )
        ) {

            adminProfileMenu.classList.add(
                "hidden"
            );
        }
    }
);


// =========================
// ADMIN PROFILE LOGOUT
// =========================

if (adminMenuLogout) {

    adminMenuLogout.addEventListener(
        "click",
        () => {

            sessionStorage.removeItem(
                TOKEN_KEY
            );


            window.location.href =
                "/";
        }
    );
}


// =========================
// SIDEBAR LOGOUT
// =========================

if (adminLogout) {

    adminLogout.addEventListener(
        "click",
        () => {

            sessionStorage.removeItem(
                TOKEN_KEY
            );


            window.location.href =
                "/";
        }
    );
}


// =========================
// ESCAPE HTML
// =========================

function escapeHtml(
    value
) {

    return String(value ?? "")
        .replaceAll(
            "&",
            "&amp;"
        )
        .replaceAll(
            "<",
            "&lt;"
        )
        .replaceAll(
            ">",
            "&gt;"
        )
        .replaceAll(
            '"',
            "&quot;"
        )
        .replaceAll(
            "'",
            "&#039;"
        );
}


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
    ).format(
        Number(price) || 0
    );
}


// =========================
// INITIALIZE
// =========================

async function initAdmin() {

    const authorized =
        await loadCurrentAdmin();


    if (!authorized) {
        return;
    }


    await loadProducts();

await loadCategories();

await loadUsers();

showSection(
    "dashboard"
);
}


initAdmin();