import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

export default api;

export async function fetchUploadBatches() {
  const res = await fetch("http://127.0.0.1:8000/api/upload-batches/");
  return res.json();
}

export async function deleteUploadBatch(id) {
  return fetch(`http://127.0.0.1:8000/api/upload-batch/${id}/`, {
    method: "DELETE",
  });
}
