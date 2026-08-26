// =========================
// DOM ELEMENTS
// =========================

const productGrid =
    document.getElementById("product-grid");

const recommendationGrid =
    document.getElementById(
        "recommendation-grid"
    );

const wishlistGrid =
    document.getElementById(
        "wishlist-grid"
    );

const productCount =
    document.getElementById(
        "product-count"
    );

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

const wishlistCount =
    document.getElementById(
        "wishlist-count"
    );

const themeToggle =
    document.getElementById(
        "theme-toggle"
    );

const categoryButtons =
    document.querySelectorAll(
        ".category-button"
    );


// =========================
// AUTH ELEMENTS
// =========================

const loginButton =
    document.getElementById(
        "login-button"
    );

const logoutButton =
    document.getElementById(
        "logout-button"
    );

const profileButton =
    document.getElementById(
        "profile-button"
    );

const userName =
    document.getElementById(
        "user-name"
    );


// =========================
// PROFILE DROPDOWN
// =========================

const profileDropdown =
    document.getElementById(
        "profile-dropdown"
    );

const dropdownUsername =
    document.getElementById(
        "dropdown-username"
    );

const dropdownEmail =
    document.getElementById(
        "dropdown-email"
    );

const dropdownProfile =
    document.getElementById(
        "dropdown-profile"
    );

const dropdownWishlist =
    document.getElementById(
        "dropdown-wishlist"
    );

const dropdownLogout =
    document.getElementById(
        "dropdown-logout"
    );


// =========================
// LOGIN MODAL
// =========================

const authModal =
    document.getElementById(
        "auth-modal"
    );

const authClose =
    document.getElementById(
        "auth-close"
    );

const loginForm =
    document.getElementById(
        "login-form"
    );

const loginMessage =
    document.getElementById(
        "login-message"
    );


// =========================
// PROFILE MODAL
// =========================

const profileModal =
    document.getElementById(
        "profile-modal"
    );

const profileClose =
    document.getElementById(
        "profile-close"
    );

const profileLogout =
    document.getElementById(
        "profile-logout"
    );

const profileUsername =
    document.getElementById(
        "profile-username"
    );

const profileEmail =
    document.getElementById(
        "profile-email"
    );

const profileRole =
    document.getElementById(
        "profile-role"
    );

const profileId =
    document.getElementById(
        "profile-id"
    );


// =========================
// APP STATE
// =========================

let products = [];

let activeCategory = "";

let wishlistIds = [];

let currentUser = null;

const TOKEN_KEY =
    "productrec_access_token";


// =========================
// TOKEN HELPERS
// =========================

function getToken() {

    return sessionStorage.getItem(
        TOKEN_KEY
    );
}


function setToken(token) {

    sessionStorage.setItem(
        TOKEN_KEY,
        token
    );
}


function clearToken() {

    sessionStorage.removeItem(
        TOKEN_KEY
    );
}


function isLoggedIn() {

    return Boolean(
        getToken()
    );
}


// =========================
// API REQUEST
// =========================

async function apiRequest(
    url,
    options = {}
) {

    const headers = {
        ...(options.headers || {})
    };

    const token =
        getToken();

    if (token) {

        headers.Authorization =
            `Bearer ${token}`;
    }

    const response =
        await fetch(
            url,
            {
                ...options,
                headers
            }
        );


    // Jangan anggap 401 dari login sebagai
    // session expired.
    if (
        response.status === 401
        &&
        !url.startsWith("/auth/login")
    ) {

        handleLogout(false);

        throw new Error(
            "Sesi login sudah berakhir. Silakan login kembali."
        );
    }


    return response;
}


// =========================
// LOGIN MODAL
// =========================

function openLoginModal() {

    if (!authModal) {
        return;
    }

    authModal.classList.remove(
        "hidden"
    );

    if (loginMessage) {

        loginMessage.textContent =
            "";
    }

    const usernameInput =
        document.getElementById(
            "login-username"
        );

    if (usernameInput) {

        usernameInput.focus();
    }
}


function closeLoginModal() {

    if (!authModal) {
        return;
    }

    authModal.classList.add(
        "hidden"
    );
}


// =========================
// PROFILE MODAL
// =========================

function openProfileModal() {

    if (!currentUser) {
        return;
    }

    updateAuthUI();

    if (profileModal) {

        profileModal.classList.remove(
            "hidden"
        );
    }
}


function closeProfileModal() {

    if (profileModal) {

        profileModal.classList.add(
            "hidden"
        );
    }
}


// =========================
// PROFILE DROPDOWN
// =========================

function openProfileDropdown() {

    if (!profileDropdown) {
        return;
    }

    profileDropdown.classList.remove(
        "hidden"
    );
}


function closeProfileDropdown() {

    if (!profileDropdown) {
        return;
    }

    profileDropdown.classList.add(
        "hidden"
    );
}


function toggleProfileDropdown() {

    if (!profileDropdown) {
        return;
    }

    profileDropdown.classList.toggle(
        "hidden"
    );
}


// =========================
// AUTH UI
// =========================

function updateAuthUI() {

    const loggedIn =
        Boolean(currentUser);


    // Login button
    if (loginButton) {

        loginButton.classList.toggle(
            "hidden",
            loggedIn
        );
    }


    // Logout button
    if (logoutButton) {

        logoutButton.classList.toggle(
            "hidden",
            !loggedIn
        );
    }


    // Profile button
    if (profileButton) {

        profileButton.classList.toggle(
            "hidden",
            !loggedIn
        );

        profileButton.textContent =
            loggedIn
                ? `👤 ${currentUser.username}`
                : "";
    }


    // Old user-name element, kalau masih ada
    if (userName) {

        userName.classList.toggle(
            "hidden",
            true
        );

        userName.textContent =
            "";
    }


    // Profile modal
    if (profileUsername) {

        profileUsername.textContent =
            loggedIn
                ? currentUser.username
                : "-";
    }


    if (profileEmail) {

        profileEmail.textContent =
            loggedIn
                ? currentUser.email
                : "-";
    }


    if (profileRole) {

        profileRole.textContent =
            loggedIn
                ? currentUser.role
                : "-";
    }


    if (profileId) {

        profileId.textContent =
            loggedIn
                ? currentUser.id
                : "-";
    }


    // Dropdown
    if (dropdownUsername) {

        dropdownUsername.textContent =
            loggedIn
                ? currentUser.username
                : "-";
    }


    if (dropdownEmail) {

        dropdownEmail.textContent =
            loggedIn
                ? currentUser.email
                : "-";
    }


    // Kalau logout, dropdown harus tutup
    if (!loggedIn) {

        closeProfileDropdown();

        closeProfileModal();
    }
}


// =========================
// LOAD CURRENT USER
// =========================

async function loadCurrentUser() {

    const token =
        getToken();


    if (!token) {

        currentUser = null;

        updateAuthUI();

        return false;
    }


    try {

        const response =
            await apiRequest(
                "/auth/me"
            );


        if (!response.ok) {

            clearToken();

            currentUser = null;

            updateAuthUI();

            return false;
        }


        currentUser =
            await response.json();


        updateAuthUI();

        return true;


    } catch (error) {

        console.error(
            "Load current user error:",
            error
        );

        clearToken();

        currentUser = null;

        updateAuthUI();

        return false;
    }
}


// =========================
// LOGIN API
// =========================

async function loginUser(
    username,
    password
) {

    const body =
        new URLSearchParams();


    body.append(
        "username",
        username
    );


    body.append(
        "password",
        password
    );


    const response =
        await fetch(
            "/auth/login",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/x-www-form-urlencoded"
                },

                body
            }
        );


    let data = {};

    try {

        data =
            await response.json();

    } catch {

        data = {};
    }


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Username atau password salah."
        );
    }


    if (!data.access_token) {

        throw new Error(
            "Token login tidak diterima."
        );
    }


    setToken(
        data.access_token
    );


    return data;
}


// =========================
// LOGOUT
// =========================

function handleLogout(
    closeModal = true
) {

    clearToken();

    currentUser = null;

    wishlistIds = [];


    updateAuthUI();

    updateWishlistCount();


    renderProducts(
        getFilteredProducts()
    );


    renderWishlist();


    if (closeModal) {

        closeLoginModal();
        closeProfileModal();
        closeProfileDropdown();
    }
}


// =========================
// LOGIN FORM
// =========================

if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            const usernameInput =
                document.getElementById(
                    "login-username"
                );

            const passwordInput =
                document.getElementById(
                    "login-password"
                );


            const username =
                usernameInput
                    ? usernameInput.value.trim()
                    : "";

            const password =
                passwordInput
                    ? passwordInput.value
                    : "";


            if (!username || !password) {

                if (loginMessage) {

                    loginMessage.textContent =
                        "Username dan password wajib diisi.";
                }

                return;
            }


            try {

                if (loginMessage) {

                    loginMessage.textContent =
                        "Memproses login...";
                }


                // 1. Login
                await loginUser(
                    username,
                    password
                );


                // 2. Ambil user berdasarkan JWT
                const userLoaded =
                    await loadCurrentUser();


                if (!userLoaded) {

                    clearToken();

                    throw new Error(
                        "Login berhasil, tetapi data user tidak dapat diambil."
                    );
                }


                // 3. Ambil wishlist
                await loadWishlistFromApi();


                // 4. Tutup modal
                closeLoginModal();


                // 5. Bersihkan form
                loginForm.reset();


                // 6. Refresh UI
                renderProducts(
                    getFilteredProducts()
                );

                renderWishlist();


            } catch (error) {

                console.error(
                    "Login error:",
                    error
                );


                clearToken();

                currentUser = null;

                wishlistIds = [];


                updateAuthUI();

                updateWishlistCount();

                renderWishlist();


                if (loginMessage) {

                    loginMessage.textContent =
                        error.message ||
                        "Login gagal.";
                }
            }
        }
    );
}


// =========================
// LOGIN BUTTON
// =========================

if (loginButton) {

    loginButton.addEventListener(
        "click",
        openLoginModal
    );
}


// =========================
// LOGOUT BUTTON
// =========================

if (logoutButton) {

    logoutButton.addEventListener(
        "click",
        event => {

            event.preventDefault();

            handleLogout(true);
        }
    );
}


// =========================
// CLOSE LOGIN
// =========================

if (authClose) {

    authClose.addEventListener(
        "click",
        closeLoginModal
    );
}


// =========================
// PROFILE BUTTON
// =========================

if (profileButton) {

    profileButton.addEventListener(
        "click",
        event => {

            event.stopPropagation();

            toggleProfileDropdown();
        }
    );
}


// =========================
// PROFILE DROPDOWN - PROFILE
// =========================

if (dropdownProfile) {

    dropdownProfile.addEventListener(
        "click",
        event => {

            event.stopPropagation();

            closeProfileDropdown();

            openProfileModal();
        }
    );
}


// =========================
// PROFILE DROPDOWN - WISHLIST
// =========================

if (dropdownWishlist) {

    dropdownWishlist.addEventListener(
        "click",
        event => {

            event.stopPropagation();

            closeProfileDropdown();

            const wishlistSection =
                document.getElementById(
                    "wishlist"
                );

            if (wishlistSection) {

                wishlistSection.scrollIntoView({
                    behavior: "smooth"
                });
            }
        }
    );
}


// =========================
// PROFILE DROPDOWN - LOGOUT
// =========================

if (dropdownLogout) {

    dropdownLogout.addEventListener(
        "click",
        event => {

            event.stopPropagation();

            closeProfileDropdown();

            handleLogout(true);
        }
    );
}


// =========================
// PROFILE MODAL - CLOSE
// =========================

if (profileClose) {

    profileClose.addEventListener(
        "click",
        closeProfileModal
    );
}


// =========================
// PROFILE MODAL - LOGOUT
// =========================

if (profileLogout) {

    profileLogout.addEventListener(
        "click",
        () => {

            closeProfileModal();

            handleLogout(true);
        }
    );
}


// =========================
// CLICK OUTSIDE PROFILE
// =========================

document.addEventListener(
    "click",
    event => {

        if (
            profileDropdown &&
            profileButton &&
            !profileDropdown.contains(
                event.target
            ) &&
            !profileButton.contains(
                event.target
            )
        ) {

            closeProfileDropdown();
        }
    }
);


// =========================
// LOAD PRODUCTS
// =========================

async function loadProducts() {

    try {

        const response =
            await fetch(
                "/products"
            );


        if (!response.ok) {

            throw new Error(
                "Gagal mengambil produk."
            );
        }


        products =
            await response.json();


        activeCategory = "";


        if (searchInput) {

            searchInput.value =
                "";
        }


        if (heroSearch) {

            heroSearch.value =
                "";
        }


        if (sortSelect) {

            sortSelect.value =
                "default";
        }


        categoryButtons.forEach(
            button =>
                button.classList.remove(
                    "active"
                )
        );


        const allButton =
            document.querySelector(
                '.category-button[data-category=""]'
            );


        if (allButton) {

            allButton.classList.add(
                "active"
            );
        }


        renderProducts(
            products
        );


        if (productCount) {

            productCount.textContent =
                `${products.length} produk tersedia`;
        }


        await loadCurrentUser();

        await loadWishlistFromApi();


    } catch (error) {

        console.error(
            "Load products error:",
            error
        );


        if (productGrid) {

            productGrid.innerHTML = `
                <div class="empty-state">

                    <div class="empty-icon">
                        ⚠️
                    </div>

                    <h3>
                        Gagal memuat produk
                    </h3>

                    <p>
                        Pastikan server API sedang berjalan.
                    </p>

                </div>
            `;
        }
    }
}


// =========================
// LOAD WISHLIST
// =========================

async function loadWishlistFromApi() {

    if (!isLoggedIn()) {

        wishlistIds = [];

        updateWishlistCount();

        renderWishlist();

        return;
    }


    try {

        const response =
            await apiRequest(
                "/wishlist"
            );


        if (!response.ok) {

            throw new Error(
                "Gagal mengambil wishlist."
            );
        }


        const data =
            await response.json();


        wishlistIds =
            data.map(
                product =>
                    Number(product.id)
            );


        updateWishlistCount();

        renderProducts(
            getFilteredProducts()
        );

        renderWishlist();


    } catch (error) {

        console.error(
            "Wishlist load error:",
            error
        );
    }
}


// =========================
// ADD WISHLIST
// =========================

async function addToWishlist(
    productId
) {

    if (!isLoggedIn()) {

        openLoginModal();

        return false;
    }


    const response =
        await apiRequest(
            `/wishlist/${productId}`,
            {
                method: "POST"
            }
        );


    let data = {};

    try {

        data =
            await response.json();

    } catch {

        data = {};
    }


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Gagal menambahkan wishlist."
        );
    }


    const numericId =
        Number(productId);


    if (
        !wishlistIds.includes(
            numericId
        )
    ) {

        wishlistIds.push(
            numericId
        );
    }


    updateWishlistCount();

    return true;
}


// =========================
// REMOVE WISHLIST
// =========================

async function removeFromWishlist(
    productId
) {

    if (!isLoggedIn()) {

        openLoginModal();

        return false;
    }


    const response =
        await apiRequest(
            `/wishlist/${productId}`,
            {
                method: "DELETE"
            }
        );


    let data = {};

    try {

        data =
            await response.json();

    } catch {

        data = {};
    }


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Gagal menghapus wishlist."
        );
    }


    const numericId =
        Number(productId);


    wishlistIds =
        wishlistIds.filter(
            id =>
                id !== numericId
        );


    updateWishlistCount();

    return true;
}


// =========================
// TOGGLE WISHLIST
// =========================

async function toggleWishlist(
    productId
) {

    try {

        if (
            isWishlisted(
                productId
            )
        ) {

            await removeFromWishlist(
                productId
            );

        } else {

            await addToWishlist(
                productId
            );
        }


        renderProducts(
            getFilteredProducts()
        );


        renderWishlist();


        const product =
            products.find(
                item =>
                    Number(item.id) ===
                    Number(productId)
            );


        if (
            product &&
            detailSection &&
            !detailSection.classList.contains(
                "hidden"
            )
        ) {

            renderProductDetail(
                product
            );
        }


    } catch (error) {

        console.error(
            "Wishlist error:",
            error
        );

        alert(
            error.message
        );
    }
}


// =========================
// WISHLIST STATE
// =========================

function isWishlisted(
    productId
) {

    return wishlistIds.includes(
        Number(productId)
    );
}


function updateWishlistCount() {

    if (!wishlistCount) {

        return;
    }


    wishlistCount.textContent =
        wishlistIds.length;
}


function renderWishlist() {

    if (!wishlistGrid) {

        return;
    }


    if (!isLoggedIn()) {

        wishlistGrid.innerHTML = `
            <div class="empty-state">

                <div class="empty-icon">
                    🔐
                </div>

                <h3>
                    Login untuk melihat wishlist
                </h3>

                <p>
                    Wishlist tersimpan
                    berdasarkan akunmu.
                </p>

            </div>
        `;

        return;
    }


    const wishlistProducts =
        products.filter(
            product =>
                isWishlisted(
                    product.id
                )
        );


    wishlistGrid.innerHTML =
        "";


    if (!wishlistProducts.length) {

        wishlistGrid.innerHTML = `
            <div class="empty-state">

                <div class="empty-icon">
                    ♡
                </div>

                <h3>
                    Wishlist masih kosong
                </h3>

                <p>
                    Simpan produk yang ingin
                    kamu lihat nanti.
                </p>

            </div>
        `;

        return;
    }


    wishlistProducts.forEach(
        product => {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "product-card";


            card.innerHTML = `
                <button
                    class="wishlist-button active"
                    type="button"
                    aria-label="Hapus dari wishlist"
                >
                    ♥
                </button>

                <div class="product-type">
                    ${escapeHtml(
                        product.kategori
                    )}
                </div>

                <h3>
                    ${escapeHtml(
                        product.nama
                    )}
                </h3>

                <div class="product-brand">
                    ${escapeHtml(
                        product.brand
                    )}
                </div>

                <div class="product-price">
                    ${formatPrice(
                        product.harga
                    )}
                </div>
            `;


            card.addEventListener(
                "click",
                () =>
                    openProduct(
                        product.id
                    )
            );


            const button =
                card.querySelector(
                    ".wishlist-button"
                );


            button.addEventListener(
                "click",
                async event => {

                    event.stopPropagation();

                    await toggleWishlist(
                        product.id
                    );
                }
            );


            wishlistGrid.appendChild(
                card
            );
        }
    );
}


// =========================
// FILTER + SORT
// =========================

function getFilteredProducts() {

    const keyword =
        searchInput
            ? searchInput.value
                .toLowerCase()
                .trim()
            : "";


    let filtered =
        products.filter(
            product => {

                const matchesKeyword =
                    !keyword
                    ||
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
                    product.kategori ===
                        activeCategory;


                return (
                    matchesKeyword &&
                    matchesCategory
                );
            }
        );


    if (sortSelect) {

        switch (
            sortSelect.value
        ) {

            case "price-low":

                filtered.sort(
                    (a, b) =>
                        a.harga -
                        b.harga
                );

                break;


            case "price-high":

                filtered.sort(
                    (a, b) =>
                        b.harga -
                        a.harga
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
    }


    return filtered;
}


function applyFilters() {

    const filtered =
        getFilteredProducts();


    renderProducts(
        filtered
    );


    if (productCount) {

        productCount.textContent =
            `${filtered.length} produk ditemukan`;
    }
}


// =========================
// RENDER PRODUCTS
// =========================

function renderProducts(
    productList
) {

    if (!productGrid) {

        return;
    }


    productGrid.innerHTML =
        "";


    if (!productList.length) {

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


    productList.forEach(
        product => {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "product-card";


            const wishlisted =
                isWishlisted(
                    product.id
                );


            card.innerHTML = `
                <button
                    class="wishlist-button ${
                        wishlisted
                            ? "active"
                            : ""
                    }"
                    type="button"
                    aria-label="${
                        wishlisted
                            ? "Hapus dari wishlist"
                            : "Tambah ke wishlist"
                    }"
                >
                    ${
                        wishlisted
                            ? "♥"
                            : "♡"
                    }
                </button>

                <div class="product-type">
                    ${escapeHtml(
                        product.kategori
                    )}
                </div>

                <h3>
                    ${escapeHtml(
                        product.nama
                    )}
                </h3>

                <div class="product-brand">
                    ${escapeHtml(
                        product.brand
                    )}
                </div>

                <div class="product-price">
                    ${formatPrice(
                        product.harga
                    )}
                </div>
            `;


            const wishlistButton =
                card.querySelector(
                    ".wishlist-button"
                );


            wishlistButton.addEventListener(
                "click",
                async event => {

                    event.stopPropagation();

                    await toggleWishlist(
                        product.id
                    );
                }
            );


            card.addEventListener(
                "click",
                () =>
                    openProduct(
                        product.id
                    )
            );


            productGrid.appendChild(
                card
            );
        }
    );
}


// =========================
// PRODUCT DETAIL
// =========================

async function openProduct(
    productId
) {

    try {

        const product =
            products.find(
                item =>
                    Number(item.id) ===
                    Number(productId)
            );


        if (!product) {

            throw new Error(
                "Produk tidak ditemukan."
            );
        }


        if (productSection) {

            productSection.classList.add(
                "hidden"
            );
        }


        if (detailSection) {

            detailSection.classList.remove(
                "hidden"
            );
        }


        renderProductDetail(
            product
        );


        if (
            recommendationGrid
        ) {

            recommendationGrid.innerHTML = `
                <div class="empty-state">

                    <p>
                        Memuat rekomendasi...
                    </p>

                </div>
            `;
        }


        const response =
            await apiRequest(
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
            data.recommendations || []
        );


        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });


    } catch (error) {

        console.error(
            "Open product error:",
            error
        );


        if (
            recommendationGrid
        ) {

            recommendationGrid.innerHTML = `
                <div class="empty-state">

                    <div class="empty-icon">
                        ⚠️
                    </div>

                    <h3>
                        Gagal memuat rekomendasi
                    </h3>

                    <p>
                        Coba lagi beberapa saat.
                    </p>

                </div>
            `;
        }
    }
}


// =========================
// PRODUCT DETAIL RENDER
// =========================

function renderProductDetail(
    product
) {

    if (!detailContent) {

        return;
    }


    const wishlisted =
        isWishlisted(
            product.id
        );


    detailContent.innerHTML = `
        <div class="product-type">
            ${escapeHtml(
                product.kategori
            )}
        </div>

        <h1>
            ${escapeHtml(
                product.nama
            )}
        </h1>

        <p class="product-brand">
            ${escapeHtml(
                product.brand
            )}
        </p>

        <p class="product-price">
            ${formatPrice(
                product.harga
            )}
        </p>

        <p class="detail-description">
            ${escapeHtml(
                product.deskripsi
            )}
        </p>

        <button
            id="detail-wishlist-button"
            class="detail-wishlist-button ${
                wishlisted
                    ? "active"
                    : ""
            }"
            type="button"
        >
            ${
                wishlisted
                    ? "♥ Tersimpan di wishlist"
                    : "♡ Tambah ke wishlist"
            }
        </button>

        <div class="specifications">

            <div class="spec-item">

                <span class="spec-label">
                    Jenis
                </span>

                ${escapeHtml(
                    product.jenis
                )}

            </div>


            <div class="spec-item">

                <span class="spec-label">
                    Kategori
                </span>

                ${escapeHtml(
                    product.kategori
                )}

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


    const button =
        document.getElementById(
            "detail-wishlist-button"
        );


    if (button) {

        button.addEventListener(
            "click",
            async () => {

                await toggleWishlist(
                    product.id
                );
            }
        );
    }
}


// =========================
// RECOMMENDATIONS
// =========================

function renderRecommendations(
    recommendations
) {

    if (!recommendationGrid) {

        return;
    }


    recommendationGrid.innerHTML =
        "";


    if (!recommendations.length) {

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
                document.createElement(
                    "div"
                );


            card.className =
                "product-card";


            const reasons =
                Array.isArray(
                    recommendation.reasons
                )
                    ? recommendation.reasons
                    : [];


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
                    ${(
                        recommendation.similarity *
                        100
                    ).toFixed(1)}%
                </div>

                ${
                    reasons.length
                        ? `
                            <div class="recommendation-reasons">

                                <div class="reason-title">
                                    Mengapa direkomendasikan?
                                </div>

                                ${reasons
                                    .map(
                                        reason => `
                                            <div class="reason-item">
                                                ✓ ${escapeHtml(
                                                    reason
                                                )}
                                            </div>
                                        `
                                    )
                                    .join("")}

                            </div>
                        `
                        : ""
                }
            `;


            card.addEventListener(
                "click",
                () =>
                    openProduct(
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

if (searchInput) {

    searchInput.addEventListener(
        "input",
        applyFilters
    );
}


if (heroSearch) {

    heroSearch.addEventListener(
        "input",
        event => {

            if (searchInput) {

                searchInput.value =
                    event.target.value;
            }

            applyFilters();
        }
    );
}


// =========================
// SORT
// =========================

if (sortSelect) {

    sortSelect.addEventListener(
        "change",
        applyFilters
    );
}


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
                    button.dataset.category ||
                    "";


                applyFilters();
            }
        );
    }
);


// =========================
// BACK BUTTON
// =========================

if (backButton) {

    backButton.addEventListener(
        "click",
        () => {

            if (detailSection) {

                detailSection.classList.add(
                    "hidden"
                );
            }


            if (productSection) {

                productSection.classList.remove(
                    "hidden"
                );
            }


            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        }
    );
}


// =========================
// THEME
// =========================

function loadTheme() {

    const savedTheme =
        localStorage.getItem(
            "productrec_theme"
        );


    setTheme(
        savedTheme === "dark"
    );
}


function setTheme(
    isDark
) {

    const html =
        document.documentElement;


    if (isDark) {

        html.setAttribute(
            "data-theme",
            "dark"
        );

    } else {

        html.removeAttribute(
            "data-theme"
        );
    }


    updateThemeButton(
        isDark
    );
}


function updateThemeButton(
    isDark
) {

    if (!themeToggle) {

        return;
    }


    themeToggle.textContent =
        isDark
            ? "☀️"
            : "🌙";


    themeToggle.setAttribute(
        "aria-label",
        isDark
            ? "Gunakan mode terang"
            : "Gunakan mode gelap"
    );
}


function toggleTheme() {

    const html =
        document.documentElement;


    const isDark =
        html.getAttribute(
            "data-theme"
        ) !== "dark";


    setTheme(
        isDark
    );


    localStorage.setItem(
        "productrec_theme",
        isDark
            ? "dark"
            : "light"
    );
}


if (themeToggle) {

    themeToggle.addEventListener(
        "click",
        toggleTheme
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
// HTML SECURITY
// =========================

function escapeHtml(
    value
) {

    return String(value)
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
// START APPLICATION
// =========================

loadTheme();

loadProducts();