"use server";
export async function submit(formData: FormData) {
  // Send the FormData to thew extraction service
  const res = await fetch("http://localhost:8000/extractor/", {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    console.error("Error attempting to extract: ", res.status, res);
    return { error: "Could not get extraction.", status: res.status };
  }

  const data = await res.json();
  return data?.data;
}
