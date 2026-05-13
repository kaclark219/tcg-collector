import { useEffect, useMemo, useState } from "react";
import { Image, ImageResizeMode, ImageStyle, StyleProp, View, ViewStyle } from "react-native";
import { buildTcgdexImageCandidates } from "@/services/tcgdexImages";

type CardImageProps = {
  imageUrl?: string;
  style?: StyleProp<ImageStyle>;
  resizeMode?: ImageResizeMode;
  placeholderStyle?: StyleProp<ViewStyle>;
};

export function CardImage({
  imageUrl,
  style,
  resizeMode = "cover",
  placeholderStyle,
}: CardImageProps) {
  const candidates = useMemo(() => buildTcgdexImageCandidates(imageUrl), [imageUrl]);
  const [candidateIndex, setCandidateIndex] = useState(0);

  useEffect(() => {
    setCandidateIndex(0);
  }, [imageUrl]);

  const activeUri = candidates[candidateIndex];

  if (!activeUri) {
    return <View style={placeholderStyle} />;
  }

  return (
    <Image
      source={{ uri: activeUri }}
      style={style}
      resizeMode={resizeMode}
      onError={() => {
        if (candidateIndex < candidates.length - 1) {
          setCandidateIndex((current) => current + 1);
        }
      }}
    />
  );
}
