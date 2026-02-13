export function SearchResults({ results }) {
  return (
    <section>
      <h3>Search</h3>
      <ul>
        {results.map((item) => (
          <li key={item.id}>
            <strong>{item.title}</strong>
            <div>{item.summary}</div>
          </li>
        ))}
      </ul>
    </section>
  );
}
