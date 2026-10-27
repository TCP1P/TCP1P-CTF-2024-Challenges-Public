import { cookies } from "next/headers";
import ImageUpload from "./image";

export const dynamic = 'force-dynamic'

export default function Page() {
  return <>
    <ImageUpload imgBlob={cookies().get("imgBlob")?.value||null}></ImageUpload>
  </>
}
