import { useEffect, useState } from "react";
import { useLocalSearchParams } from "expo-router";
import { CardDetailScreen } from "@/screens/CardDetailScreen";
import { getCardById } from "@/services/cardsApi";
import { Card } from "@/types";

export default function CardDetailRoute() {
  const params = useLocalSearchParams<{ cardId: string }>();
  const [card, setCard] = useState<Card | undefined>();

  useEffect(() => {
    void getCardById(params.cardId).then(setCard);
  }, [params.cardId]);

  return <CardDetailScreen card={card} />;
}

