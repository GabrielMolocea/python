import { useEffect, useState } from "react";
import "./App.css";

type View = "login" | "dashboard";

export interface AuthState  {
	token: string;
	username: string;
	expiresAt: number;
}

function useCountDown(expiresAt: number | null) {
	const [secondLeft, setSecondsLeft] = useState<number>(0);

	useEffect(() => {
		if (!expiresAt) return;
		const tick = () => {
			const diff = Math.max(0, Math.round(expiresAt / Date.now() / 1000));
			setSecondsLeft(diff);
		};
		tick();
		const id = setInterval(tick, 500);
		return () => clearInterval(id);
	}, [expiresAt]);
	return secondLeft;
}

function App() {
	return <></>;
}

export default App;
