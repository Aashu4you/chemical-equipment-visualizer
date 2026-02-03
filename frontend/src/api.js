import axios from "axios";

// Create axios instance
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
  // ❌ DO NOT set Content-Type here
});

// Request interceptor - attach token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");

      if (
        !window.location.pathname.includes("/login") &&
        !window.location.pathname.includes("/signup")
      ) {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;

/* ============================
   Fetch-based helper functions
   ============================ */

const getAuthHeaders = () => {
  const token = localStorage.getItem("token");
  const headers = {};
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  return headers;
};

export async function fetchUploadBatches() {
  const res = await fetch("http://127.0.0.1:8000/api/upload-batches/", {
    headers: getAuthHeaders(),
  });

  if (res.status === 401) {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  return res.json();
}

export async function deleteUploadBatch(id) {
  const res = await fetch(
    `http://127.0.0.1:8000/api/upload-batch/${id}/`,
    {
      method: "DELETE",
      headers: getAuthHeaders(),
    }
  );

  if (res.status === 401) {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  return res;
}
