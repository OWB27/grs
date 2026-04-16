import { useState } from "react";
import { useTranslation } from "react-i18next";

import DebugToggleButton from "../ui/DebugToggleButton";
import SteamButton from "../ui/SteamButton";
import DebugPanel from "./DebugPanel";
import RecommendationCard from "./RecommendationCard";

export default function RecommendationDebugCard({ item, lang }) {
  const { t } = useTranslation();
  const [isDebugOpen, setIsDebugOpen] = useState(false);

  return (
    <RecommendationCard
      item={item}
      lang={lang}
      actions={
        <>
          <SteamButton href={item.steamUrl} />
          <DebugToggleButton
            isOpen={isDebugOpen}
            onClick={() => setIsDebugOpen((prev) => !prev)}
            ariaLabel={isDebugOpen ? t("debug.collapse") : t("debug.expand")}
          />
        </>
      }
    >
      {isDebugOpen ? <DebugPanel debug={item?.debug} gameId={item.gameId} /> : null}
    </RecommendationCard>
  );
}
