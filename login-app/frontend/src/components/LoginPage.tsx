import { use, useState } from "react";
import type { AuthState } from "../App";

function LoginPage({ oneLogin }: { oneLogin: (auth: AuthState) => void }) {
  const [loding, setLoding] = useState<Boolean>(false)
  const [shake, setShake] = useState<Boolean>(false)
  const [error, setError] = useState<string>("")
  
}
