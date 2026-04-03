"use client";

import { useCallback, useEffect, useRef, useState } from "react";

type UseMediaRecorderResult = {
  recording: boolean;
  audioBlob: Blob | null;
  audioURL: string | null;
  error: string | null;
  startRecording: () => Promise<void>;
  stopRecording: () => void;
  reset: () => void;
};

function pickRecorderMimeType(): string | undefined {
  if (typeof MediaRecorder === "undefined" || !MediaRecorder.isTypeSupported)
    return undefined;
  const candidates = [
    "audio/webm;codecs=opus",
    "audio/webm",
    "audio/mp4",
    "audio/ogg;codecs=opus",
  ];
  for (const t of candidates) {
    if (MediaRecorder.isTypeSupported(t)) return t;
  }
  return undefined;
}

export function useMediaRecorder(): UseMediaRecorderResult {
  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioURL, setAudioURL] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const mimeTypeRef = useRef<string>("audio/webm");
  /** Keeps latest object URL for revoke without making reset() depend on audioURL state (avoids spurious effect runs in parents). */
  const audioURLRef = useRef<string | null>(null);

  const revokeAudioURL = useCallback((url: string | null) => {
    if (!url) return;
    try {
      URL.revokeObjectURL(url);
    } catch {
      // ignore
    }
  }, []);

  const stopStreamTracks = useCallback(() => {
    const stream = streamRef.current;
    if (!stream) return;
    stream.getTracks().forEach((t) => {
      try {
        t.stop();
      } catch {
        // ignore
      }
    });
    streamRef.current = null;
  }, []);

  const reset = useCallback(() => {
    setRecording(false);
    setError(null);
    setAudioBlob(null);
    revokeAudioURL(audioURLRef.current);
    audioURLRef.current = null;
    setAudioURL(null);

    const recorder = mediaRecorderRef.current;
    if (recorder) {
      recorder.ondataavailable = null;
      recorder.onstop = null;
      if (recorder.state === "recording" || recorder.state === "paused") {
        try {
          recorder.stop();
        } catch {
          // ignore
        }
      }
    }
    mediaRecorderRef.current = null;
    stopStreamTracks();
    chunksRef.current = [];
  }, [revokeAudioURL, stopStreamTracks]);

  useEffect(() => {
    return () => reset();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const startRecording = useCallback(async () => {
    setError(null);
    setAudioBlob(null);
    revokeAudioURL(audioURLRef.current);
    audioURLRef.current = null;
    setAudioURL(null);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      const mimeType = pickRecorderMimeType();
      mimeTypeRef.current = mimeType || "audio/webm";

      const recorder = mimeType
        ? new MediaRecorder(stream, { mimeType })
        : new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      chunksRef.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) chunksRef.current.push(e.data);
      };

      recorder.onstop = () => {
        stopStreamTracks();
        const type =
          recorder.mimeType && recorder.mimeType.length > 0
            ? recorder.mimeType
            : mimeTypeRef.current;
        const blob = new Blob(chunksRef.current, { type });
        chunksRef.current = [];
        mediaRecorderRef.current = null;
        setAudioBlob(blob);
        const url = URL.createObjectURL(blob);
        audioURLRef.current = url;
        setAudioURL(url);
        setRecording(false);
      };

      recorder.start(100);
      setRecording(true);
    } catch {
      setError("Microphone access denied or unavailable.");
    }
  }, [revokeAudioURL, stopStreamTracks]);

  const stopRecording = useCallback(() => {
    const recorder = mediaRecorderRef.current;
    if (!recorder) return;

    if (recorder.state === "recording") {
      try {
        recorder.requestData();
      } catch {
        // ignore
      }
      try {
        recorder.stop();
      } catch {
        // ignore
      }
    }
  }, []);

  return {
    recording,
    audioBlob,
    audioURL,
    error,
    startRecording,
    stopRecording,
    reset,
  };
}
