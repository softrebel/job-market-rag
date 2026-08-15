from qdrant_client.models import ScoredPoint

from app.domain.search_result import SearchResult


class JobResultAggregator:
    def aggregate(
        self,
        points: list[ScoredPoint],
    ) -> list[SearchResult]:

        jobs: dict[str, SearchResult] = {}

        for point in points:
            payload = point.payload or {}

            job_id = payload.get("job_id")

            if job_id is None:
                continue

            job_id = str(job_id)

            score = float(point.score)

            existing = jobs.get(job_id)

            # اگر این Job قبلاً دیده شده،
            # فقط بهترین chunk را نگه می‌داریم.
            if existing is not None:
                if score <= existing.score:
                    continue

            jobs[job_id] = SearchResult(
                job_id=job_id,
                title=str(payload.get("title", "")),
                company=str(payload.get("company", "")),
                text=payload.get("text"),
                city=payload.get("city"),
                score=score,
                source=payload.get("source"),
                url=payload.get("url"),
                chunk_id=str(point.id),
                metadata=payload,
            )

        results = list(jobs.values())

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results
